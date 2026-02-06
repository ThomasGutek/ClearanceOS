import time
from datetime import datetime, timedelta
from models import LegacyStatus, AdjudicationDecision
from typing import Dict, Optional
import json


class AntiCorruptionLayer:
    """
    The ACL manages the impedance mismatch between:
    - ClearanceOS (real-time, modern) 
    - Legacy NBIS Mainframe (batch-processed, SOAP/XML)
    
    Key Responsibilities:
    1. Buffer real-time decisions in local cache
    2. Translate modern JSON to legacy XML formats
    3. Simulate the "sync lag" that exists in production
    4. Provide dual-status visibility to users
    """
    
    def __init__(self, sync_interval_hours: int = 96):
        self.sync_interval = sync_interval_hours
        self.pending_queue = []
        self.status_cache: Dict[str, LegacyStatus] = {}
        self.last_batch_sync = None
    
    def publish_decision(
        self, 
        subject_id: str, 
        decision: AdjudicationDecision
    ) -> LegacyStatus:
        """
        Publishes a decision to the local cache and queues for legacy sync.
        
        Returns the dual-status object showing the real-time vs. mainframe state.
        """
        # Translate recommendation to clearance status
        status_map = {
            "GRANT": "ACTIVE",
            "DENY": "PENDING",
            "REVOKE": "REVOKED",
            "MANUAL_REVIEW": "SUSPENDED"
        }
        
        local_status = status_map.get(decision.recommendation, "PENDING")
        
        # Create dual-status object
        status = LegacyStatus(
            local_status=local_status,
            mainframe_status="ACTIVE",  # Assume currently active until synced
            last_sync=None,
            sync_lag_hours=self.sync_interval
        )
        
        # Cache locally (immediate)
        self.status_cache[subject_id] = status
        
        # Queue for batch processing
        self.pending_queue.append({
            "subject_id": subject_id,
            "decision": decision,
            "queued_at": datetime.now().isoformat(),
            "xml_payload": self._generate_soap_envelope(subject_id, decision)
        })
        
        return status
    
    def force_sync(self, subject_id: str) -> LegacyStatus:
        """
        Simulates a forced sync to the legacy mainframe.
        In production, this would actually call the SOAP endpoint.
        """
        if subject_id not in self.status_cache:
            raise ValueError(f"No cached status for subject {subject_id}")
        
        status = self.status_cache[subject_id]
        
        # Simulate network delay
        time.sleep(0.5)
        
        # "Sync" the mainframe status to match local
        status.mainframe_status = status.local_status
        status.last_sync = datetime.now().isoformat()
        status.sync_lag_hours = 0
        
        # Remove from pending queue
        self.pending_queue = [
            item for item in self.pending_queue 
            if item["subject_id"] != subject_id
        ]
        
        self.last_batch_sync = datetime.now()
        
        return status
    
    def get_status(self, subject_id: str) -> Optional[LegacyStatus]:
        """Retrieve current dual-status for a subject"""
        return self.status_cache.get(subject_id)
    
    def get_sync_queue_size(self) -> int:
        """Returns count of pending sync operations"""
        return len(self.pending_queue)
    
    def _generate_soap_envelope(
        self, 
        subject_id: str, 
        decision: AdjudicationDecision
    ) -> str:
        """
        Generates a mock SOAP/XML envelope.
        In production, this would match the actual NBIS schema.
        """
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <MessageID>{int(time.time())}</MessageID>
    <Timestamp>{datetime.now().isoformat()}</Timestamp>
  </soap:Header>
  <soap:Body>
    <ClearanceStatusUpdate xmlns="http://nbis.gov/schema/clearance/v2">
      <SubjectID>{subject_id}</SubjectID>
      <NewStatus>{decision.recommendation}</NewStatus>
      <RiskScore>{decision.risk_score}</RiskScore>
      <Justification>
        <StatementOfReasons>
          <![CDATA[{decision.generated_sor}]]>
        </StatementOfReasons>
      </Justification>
      <Citations>
"""
        
        for citation in decision.citations:
            xml += f"""        <Citation>
          <Guideline>{citation.guideline}</Guideline>
          <Source>{citation.source_paragraph}</Source>
        </Citation>
"""
        
        xml += """      </Citations>
    </ClearanceStatusUpdate>
  </soap:Body>
</soap:Envelope>"""
        
        return xml
    
    def simulate_batch_processing(self) -> int:
        """
        Simulates the nightly batch job that would sync all pending items.
        Returns number of items processed.
        """
        processed = 0
        
        for item in self.pending_queue[:]:  # Copy list to allow removal
            subject_id = item["subject_id"]
            
            # Simulate processing time
            time.sleep(0.1)
            
            # Update mainframe status
            if subject_id in self.status_cache:
                status = self.status_cache[subject_id]
                status.mainframe_status = status.local_status
                status.last_sync = datetime.now().isoformat()
                status.sync_lag_hours = 0
                processed += 1
        
        self.pending_queue.clear()
        self.last_batch_sync = datetime.now()
        
        return processed


# Global singleton instance
_acl_instance = None

def get_acl() -> AntiCorruptionLayer:
    """Returns the global ACL instance"""
    global _acl_instance
    if _acl_instance is None:
        _acl_instance = AntiCorruptionLayer()
    return _acl_instance


if __name__ == "__main__":
    print("Testing Anti-Corruption Layer...")
    
    from logic import adjudicate_case
    from ingest import simulate_vlm_extraction
    
    # Create test scenario
    acl = AntiCorruptionLayer(sync_interval_hours=96)
    
    # Simulate a decision
    incident = simulate_vlm_extraction(b"fake", "test.pdf")
    decision = adjudicate_case(incident)
    
    print(f"\n1. Publishing decision: {decision.recommendation}")
    status = acl.publish_decision("SUBJ-12345", decision)
    
    print(f"   Local Status: {status.local_status}")
    print(f"   Mainframe Status: {status.mainframe_status}")
    print(f"   Sync Lag: {status.sync_lag_hours} hours")
    
    print(f"\n2. Queue Size: {acl.get_sync_queue_size()} pending")
    
    print(f"\n3. Forcing sync...")
    synced_status = acl.force_sync("SUBJ-12345")
    print(f"   Mainframe Status: {synced_status.mainframe_status} (synced!)")
    print(f"   Queue Size: {acl.get_sync_queue_size()} pending")
    
    print("\n✓ ACL test complete")