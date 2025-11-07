#!/usr/bin/env python3
"""
AI Legal Document Generator Module
Automated Contract Generation & Compliance System
Powered by Claude AI
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
import hashlib


class DocumentType(Enum):
    """Supported legal document types"""
    NDA = "nda"
    SERVICE_AGREEMENT = "service_agreement"
    EMPLOYMENT_CONTRACT = "employment_contract"
    TERMS_OF_SERVICE = "terms_of_service"
    PRIVACY_POLICY = "privacy_policy"
    CONSULTING_AGREEMENT = "consulting_agreement"
    PARTNERSHIP_AGREEMENT = "partnership_agreement"
    LICENSING_AGREEMENT = "licensing_agreement"
    LEASE_AGREEMENT = "lease_agreement"
    INDEPENDENT_CONTRACTOR = "independent_contractor"


class USState(Enum):
    """US States for jurisdiction-specific customization"""
    CALIFORNIA = "CA"
    NEW_YORK = "NY"
    TEXAS = "TX"
    FLORIDA = "FL"
    ILLINOIS = "IL"
    PENNSYLVANIA = "PA"
    OHIO = "OH"
    GEORGIA = "GA"
    NORTH_CAROLINA = "NC"
    MICHIGAN = "MI"
    # Add more states as needed
    GENERAL = "GENERAL"


class ComplianceStatus(Enum):
    """Compliance check status"""
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    PENDING = "pending"


@dataclass
class Party:
    """Represents a party in a legal agreement"""
    name: str
    entity_type: str  # Individual, LLC, Corporation, etc.
    address: str
    email: str
    phone: Optional[str] = None
    state: Optional[str] = None
    ein_or_ssn: Optional[str] = None


@dataclass
class DocumentParameters:
    """Parameters for document generation"""
    document_type: DocumentType
    party_a: Party
    party_b: Party
    effective_date: str
    jurisdiction: USState
    custom_clauses: List[str] = field(default_factory=list)
    confidentiality_period: Optional[int] = None  # in years
    compensation: Optional[str] = None
    termination_notice_days: Optional[int] = None
    additional_terms: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceIssue:
    """Represents a compliance issue found in document"""
    severity: str  # critical, warning, info
    category: str
    description: str
    location: str
    recommendation: str


@dataclass
class GeneratedDocument:
    """Generated legal document with metadata"""
    document_id: str
    document_type: DocumentType
    content: str
    parameters: DocumentParameters
    jurisdiction: USState
    generated_at: datetime
    compliance_status: ComplianceStatus
    compliance_issues: List[ComplianceIssue]
    version: int
    hash: str
    esignature_ready: bool


class DocumentTemplateEngine:
    """Template engine for legal documents with state-specific variations"""

    def __init__(self):
        self.templates = self._initialize_templates()
        self.state_specific_clauses = self._initialize_state_clauses()

    def _initialize_templates(self) -> Dict[DocumentType, str]:
        """Initialize document templates"""
        return {
            DocumentType.NDA: """
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (the "Agreement") is entered into as of {effective_date} (the "Effective Date") by and between:

PARTY A: {party_a_name}, a {party_a_type} with a principal place of business at {party_a_address} ("Disclosing Party")

PARTY B: {party_b_name}, a {party_b_type} with a principal place of business at {party_b_address} ("Receiving Party")

RECITALS

WHEREAS, the Disclosing Party possesses certain confidential and proprietary information;
WHEREAS, the Receiving Party desires to receive such confidential information for the purpose of {purpose};

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any and all non-public information, technical data, trade secrets, or know-how disclosed by the Disclosing Party.

2. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party shall:
   a) Maintain the confidentiality of the Confidential Information
   b) Not disclose Confidential Information to any third party without prior written consent
   c) Use the Confidential Information solely for the agreed purpose
   d) Protect the Confidential Information with the same degree of care used for its own confidential information

3. TERM
This Agreement shall remain in effect for {confidentiality_period} years from the Effective Date.

4. RETURN OF MATERIALS
Upon termination, the Receiving Party shall return or destroy all Confidential Information.

5. GOVERNING LAW
This Agreement shall be governed by the laws of the State of {jurisdiction}.

{state_specific_clauses}

{custom_clauses}

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

DISCLOSING PARTY: {party_a_name}

By: _________________________
Name: {party_a_name}
Title:
Date:

RECEIVING PARTY: {party_b_name}

By: _________________________
Name: {party_b_name}
Title:
Date:
""",

            DocumentType.SERVICE_AGREEMENT: """
SERVICE AGREEMENT

This Service Agreement (the "Agreement") is entered into as of {effective_date} by and between:

SERVICE PROVIDER: {party_a_name}, a {party_a_type} located at {party_a_address} ("Provider")

CLIENT: {party_b_name}, a {party_b_type} located at {party_b_address} ("Client")

1. SERVICES
The Provider agrees to provide the following services: {services_description}

2. COMPENSATION
Client agrees to pay Provider {compensation} for the services rendered.

3. PAYMENT TERMS
{payment_terms}

4. TERM AND TERMINATION
This Agreement shall commence on {effective_date} and continue until terminated by either party with {termination_notice_days} days written notice.

5. INDEPENDENT CONTRACTOR
Provider is an independent contractor and not an employee of Client.

6. CONFIDENTIALITY
Both parties agree to maintain the confidentiality of proprietary information.

7. INTELLECTUAL PROPERTY
{ip_clause}

8. WARRANTIES AND REPRESENTATIONS
Provider warrants that services will be performed in a professional manner.

9. LIMITATION OF LIABILITY
{liability_clause}

10. GOVERNING LAW
This Agreement shall be governed by the laws of the State of {jurisdiction}.

{state_specific_clauses}

{custom_clauses}

IN WITNESS WHEREOF, the parties have executed this Agreement.

PROVIDER: {party_a_name}
Signature: _________________________
Date:

CLIENT: {party_b_name}
Signature: _________________________
Date:
""",

            DocumentType.INDEPENDENT_CONTRACTOR: """
INDEPENDENT CONTRACTOR AGREEMENT

This Independent Contractor Agreement (the "Agreement") is made as of {effective_date} between:

COMPANY: {party_a_name}, a {party_a_type} ("Company")
Address: {party_a_address}

CONTRACTOR: {party_b_name}, a {party_b_type} ("Contractor")
Address: {party_b_address}

1. SERVICES
Contractor agrees to provide the following services: {services_description}

2. COMPENSATION
Company shall pay Contractor {compensation}.

3. INDEPENDENT CONTRACTOR STATUS
Contractor is an independent contractor and not an employee. Contractor is responsible for all taxes, insurance, and benefits.

4. WORK SCHEDULE
Contractor shall determine when and where to perform services.

5. EQUIPMENT AND SUPPLIES
{equipment_clause}

6. TERM
This Agreement begins on {effective_date} and continues until terminated with {termination_notice_days} days notice.

7. INTELLECTUAL PROPERTY
All work product created by Contractor shall be the exclusive property of Company.

8. CONFIDENTIALITY
Contractor agrees to maintain confidentiality of all Company information.

9. NON-COMPETE
{non_compete_clause}

10. GOVERNING LAW
This Agreement is governed by the laws of the State of {jurisdiction}.

{state_specific_clauses}

{custom_clauses}

IN WITNESS WHEREOF, the parties have executed this Agreement.

COMPANY: {party_a_name}
Signature: _________________________
Date:

CONTRACTOR: {party_b_name}
Signature: _________________________
Date:
"""
        }

    def _initialize_state_clauses(self) -> Dict[USState, Dict[str, str]]:
        """Initialize state-specific legal clauses"""
        return {
            USState.CALIFORNIA: {
                "non_compete": "Note: Non-compete clauses are generally unenforceable in California under Business and Professions Code Section 16600.",
                "employment": "This agreement complies with California Labor Code requirements.",
                "arbitration": "Any arbitration shall be conducted in accordance with California Code of Civil Procedure Section 1280 et seq."
            },
            USState.NEW_YORK: {
                "non_compete": "Non-compete clauses must be reasonable in time, scope, and geography under New York law.",
                "employment": "This agreement complies with New York Labor Law.",
                "arbitration": "Arbitration shall be conducted under New York Civil Practice Law and Rules."
            },
            USState.TEXAS: {
                "non_compete": "Non-compete agreements must be ancillary to an otherwise enforceable agreement under Texas Business and Commerce Code Section 15.50.",
                "choice_of_law": "The parties agree that Texas law governs this agreement."
            },
            USState.GENERAL: {
                "standard": "This agreement is drafted to comply with generally applicable U.S. contract law principles."
            }
        }

    def get_template(self, doc_type: DocumentType) -> str:
        """Get template for document type"""
        return self.templates.get(doc_type, "")

    def get_state_clauses(self, state: USState) -> str:
        """Get state-specific clauses"""
        clauses = self.state_specific_clauses.get(state, {})
        if not clauses:
            clauses = self.state_specific_clauses[USState.GENERAL]

        formatted = "\nSTATE-SPECIFIC PROVISIONS:\n"
        for key, value in clauses.items():
            formatted += f"- {value}\n"

        return formatted


class ComplianceChecker:
    """AI-powered compliance checking system"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def check_compliance(
        self,
        document: str,
        document_type: DocumentType,
        jurisdiction: USState
    ) -> Tuple[ComplianceStatus, List[ComplianceIssue]]:
        """Check document for compliance issues"""

        compliance_prompt = f"""Analyze this {document_type.value} legal document for compliance issues.
Focus on:
1. Missing required clauses
2. Ambiguous language
3. Potential enforceability issues
4. Jurisdiction-specific compliance ({jurisdiction.value})
5. Standard legal requirements

Document:
{document}

Provide a JSON response with:
- overall_status: "passed", "warning", or "failed"
- issues: array of {{severity, category, description, location, recommendation}}
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": compliance_prompt
                }]
            )

            # Parse AI response
            result = response.content[0].text

            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                else:
                    # Fallback if no JSON found
                    parsed = {
                        "overall_status": "warning",
                        "issues": [{
                            "severity": "info",
                            "category": "review",
                            "description": "AI compliance check completed",
                            "location": "general",
                            "recommendation": result[:500]
                        }]
                    }
            except json.JSONDecodeError:
                parsed = {
                    "overall_status": "warning",
                    "issues": [{
                        "severity": "info",
                        "category": "review",
                        "description": "Manual review recommended",
                        "location": "general",
                        "recommendation": result[:500]
                    }]
                }

            # Convert to ComplianceIssue objects
            issues = [
                ComplianceIssue(
                    severity=issue.get("severity", "info"),
                    category=issue.get("category", "general"),
                    description=issue.get("description", ""),
                    location=issue.get("location", ""),
                    recommendation=issue.get("recommendation", "")
                )
                for issue in parsed.get("issues", [])
            ]

            status_map = {
                "passed": ComplianceStatus.PASSED,
                "warning": ComplianceStatus.WARNING,
                "failed": ComplianceStatus.FAILED
            }
            status = status_map.get(parsed.get("overall_status", "warning"), ComplianceStatus.WARNING)

            return status, issues

        except Exception as e:
            # Return warning status on error
            return ComplianceStatus.WARNING, [
                ComplianceIssue(
                    severity="warning",
                    category="system",
                    description=f"Compliance check error: {str(e)}",
                    location="system",
                    recommendation="Manual legal review recommended"
                )
            ]


class ESignatureIntegration:
    """Integration with e-signature services (DocuSign, etc.)"""

    def __init__(self):
        self.pending_signatures = {}

    def prepare_for_esignature(self, document: GeneratedDocument) -> Dict[str, Any]:
        """Prepare document for e-signature"""

        # Create signature placeholders
        signature_fields = self._extract_signature_fields(document.content)

        return {
            "document_id": document.document_id,
            "signature_fields": signature_fields,
            "signers": [
                {
                    "name": document.parameters.party_a.name,
                    "email": document.parameters.party_a.email,
                    "role": "Party A"
                },
                {
                    "name": document.parameters.party_b.name,
                    "email": document.parameters.party_b.email,
                    "role": "Party B"
                }
            ],
            "redirect_url": f"/documents/{document.document_id}/complete",
            "expiration_days": 30
        }

    def _extract_signature_fields(self, content: str) -> List[Dict[str, Any]]:
        """Extract signature field locations from document"""
        fields = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            if 'Signature:' in line or 'By:' in line:
                fields.append({
                    "type": "signature",
                    "line_number": i + 1,
                    "field_name": f"signature_{len(fields) + 1}"
                })
            elif 'Date:' in line and i > 0 and ('Signature:' in lines[i-1] or 'By:' in lines[i-1]):
                fields.append({
                    "type": "date",
                    "line_number": i + 1,
                    "field_name": f"date_{len(fields) + 1}"
                })

        return fields

    def send_for_signature(self, document_id: str, signers: List[Dict]) -> str:
        """Send document for e-signature (mock implementation)"""
        envelope_id = f"env_{int(datetime.now().timestamp())}"

        self.pending_signatures[envelope_id] = {
            "document_id": document_id,
            "signers": signers,
            "status": "sent",
            "created_at": datetime.now().isoformat()
        }

        return envelope_id

    def check_signature_status(self, envelope_id: str) -> Dict[str, Any]:
        """Check status of e-signature envelope"""
        return self.pending_signatures.get(envelope_id, {
            "status": "not_found"
        })


class AILegalDocumentGenerator:
    """Main class for AI-powered legal document generation"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize document generator"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.template_engine = DocumentTemplateEngine()
        self.compliance_checker = ComplianceChecker(self.api_key)
        self.esignature = ESignatureIntegration()

        self.documents: Dict[str, GeneratedDocument] = {}
        self.model = "claude-3-5-sonnet-20241022"

    def generate_document(
        self,
        parameters: DocumentParameters,
        use_ai_enhancement: bool = True
    ) -> GeneratedDocument:
        """Generate a legal document from parameters"""

        # Get base template
        template = self.template_engine.get_template(parameters.document_type)
        if not template:
            raise ValueError(f"Unsupported document type: {parameters.document_type}")

        # Get state-specific clauses
        state_clauses = self.template_engine.get_state_clauses(parameters.jurisdiction)

        # Prepare template variables
        variables = {
            "effective_date": parameters.effective_date,
            "party_a_name": parameters.party_a.name,
            "party_a_type": parameters.party_a.entity_type,
            "party_a_address": parameters.party_a.address,
            "party_b_name": parameters.party_b.name,
            "party_b_type": parameters.party_b.entity_type,
            "party_b_address": parameters.party_b.address,
            "jurisdiction": parameters.jurisdiction.value,
            "state_specific_clauses": state_clauses,
            "custom_clauses": "\n".join(parameters.custom_clauses) if parameters.custom_clauses else "",
            "confidentiality_period": str(parameters.confidentiality_period or 5),
            "compensation": parameters.compensation or "As mutually agreed",
            "termination_notice_days": str(parameters.termination_notice_days or 30),
            "purpose": parameters.additional_terms.get("purpose", "evaluation of business relationship"),
            "services_description": parameters.additional_terms.get("services", "Services as described in attached SOW"),
            "payment_terms": parameters.additional_terms.get("payment_terms", "Net 30 days from invoice date"),
            "ip_clause": parameters.additional_terms.get("ip_clause", "All work product becomes property of Client"),
            "liability_clause": parameters.additional_terms.get("liability_clause", "Limited to fees paid under this Agreement"),
            "equipment_clause": parameters.additional_terms.get("equipment", "Contractor provides own equipment"),
            "non_compete_clause": parameters.additional_terms.get("non_compete", "As permitted by applicable law")
        }

        # Fill in template
        document_content = template
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            document_content = document_content.replace(placeholder, str(value))

        # Enhance with AI if requested
        if use_ai_enhancement:
            document_content = self._ai_enhance_document(
                document_content,
                parameters.document_type,
                parameters.jurisdiction
            )

        # Run compliance check
        compliance_status, compliance_issues = self.compliance_checker.check_compliance(
            document_content,
            parameters.document_type,
            parameters.jurisdiction
        )

        # Generate document ID and hash
        document_id = f"doc_{int(datetime.now().timestamp())}_{parameters.document_type.value}"
        doc_hash = hashlib.sha256(document_content.encode()).hexdigest()

        # Create GeneratedDocument object
        generated_doc = GeneratedDocument(
            document_id=document_id,
            document_type=parameters.document_type,
            content=document_content,
            parameters=parameters,
            jurisdiction=parameters.jurisdiction,
            generated_at=datetime.now(),
            compliance_status=compliance_status,
            compliance_issues=compliance_issues,
            version=1,
            hash=doc_hash,
            esignature_ready=True
        )

        # Store document
        self.documents[document_id] = generated_doc

        return generated_doc

    def _ai_enhance_document(
        self,
        document: str,
        doc_type: DocumentType,
        jurisdiction: USState
    ) -> str:
        """Use AI to enhance and refine the document"""

        enhancement_prompt = f"""Review and enhance this {doc_type.value} legal document for the jurisdiction of {jurisdiction.value}.

Make improvements for:
1. Legal clarity and precision
2. Enforceability
3. Completeness
4. Professional formatting
5. Jurisdiction-specific requirements

Return the enhanced document. Make minimal changes - only improve clarity and legal soundness.

Document:
{document}

Enhanced Document:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": enhancement_prompt
                }]
            )

            enhanced = response.content[0].text.strip()

            # If AI response is substantially longer or shorter, keep original
            if len(enhanced) > len(document) * 1.5 or len(enhanced) < len(document) * 0.5:
                return document

            return enhanced

        except Exception as e:
            print(f"AI enhancement failed: {e}")
            return document

    def customize_document(
        self,
        document_id: str,
        custom_modifications: str
    ) -> GeneratedDocument:
        """Customize an existing document with AI assistance"""

        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")

        original_doc = self.documents[document_id]

        customization_prompt = f"""Apply the following customizations to this legal document:

Customizations requested:
{custom_modifications}

Original document:
{original_doc.content}

Return the customized document:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": customization_prompt
                }]
            )

            customized_content = response.content[0].text.strip()

            # Re-check compliance
            compliance_status, compliance_issues = self.compliance_checker.check_compliance(
                customized_content,
                original_doc.document_type,
                original_doc.jurisdiction
            )

            # Create new version
            new_doc_id = f"{document_id}_v{original_doc.version + 1}"
            new_hash = hashlib.sha256(customized_content.encode()).hexdigest()

            customized_doc = GeneratedDocument(
                document_id=new_doc_id,
                document_type=original_doc.document_type,
                content=customized_content,
                parameters=original_doc.parameters,
                jurisdiction=original_doc.jurisdiction,
                generated_at=datetime.now(),
                compliance_status=compliance_status,
                compliance_issues=compliance_issues,
                version=original_doc.version + 1,
                hash=new_hash,
                esignature_ready=True
            )

            self.documents[new_doc_id] = customized_doc
            return customized_doc

        except Exception as e:
            raise Exception(f"Customization failed: {e}")

    def prepare_for_signature(self, document_id: str) -> Dict[str, Any]:
        """Prepare document for e-signature"""
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")

        document = self.documents[document_id]
        return self.esignature.prepare_for_esignature(document)

    def export_document(
        self,
        document_id: str,
        format: str = "txt"
    ) -> str:
        """Export document in specified format"""
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")

        document = self.documents[document_id]

        if format == "txt":
            return document.content
        elif format == "json":
            return json.dumps({
                "document_id": document.document_id,
                "type": document.document_type.value,
                "content": document.content,
                "jurisdiction": document.jurisdiction.value,
                "generated_at": document.generated_at.isoformat(),
                "compliance_status": document.compliance_status.value,
                "version": document.version,
                "hash": document.hash
            }, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics about generated documents"""
        total_docs = len(self.documents)

        # Document type distribution
        type_dist = {}
        for doc in self.documents.values():
            doc_type = doc.document_type.value
            type_dist[doc_type] = type_dist.get(doc_type, 0) + 1

        # Compliance status distribution
        compliance_dist = {}
        for doc in self.documents.values():
            status = doc.compliance_status.value
            compliance_dist[status] = compliance_dist.get(status, 0) + 1

        # Jurisdiction distribution
        jurisdiction_dist = {}
        for doc in self.documents.values():
            jurisdiction = doc.jurisdiction.value
            jurisdiction_dist[jurisdiction] = jurisdiction_dist.get(jurisdiction, 0) + 1

        return {
            "total_documents": total_docs,
            "document_types": type_dist,
            "compliance_status": compliance_dist,
            "jurisdictions": jurisdiction_dist,
            "average_compliance_issues": sum(
                len(doc.compliance_issues) for doc in self.documents.values()
            ) / total_docs if total_docs > 0 else 0
        }


def demo_legal_generator():
    """Demo function showing legal document generator capabilities"""
    print("=" * 80)
    print("AI Legal Document Generator - Demo")
    print("=" * 80)

    # Initialize generator
    try:
        generator = AILegalDocumentGenerator()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Create parties
    party_a = Party(
        name="TechCorp Inc.",
        entity_type="Delaware Corporation",
        address="123 Tech Street, San Francisco, CA 94105",
        email="legal@techcorp.com",
        state="CA"
    )

    party_b = Party(
        name="Innovation Labs LLC",
        entity_type="Limited Liability Company",
        address="456 Innovation Ave, Austin, TX 78701",
        email="contracts@innovationlabs.com",
        state="TX"
    )

    print("\n📄 Generating NDA...")

    # Generate NDA
    nda_params = DocumentParameters(
        document_type=DocumentType.NDA,
        party_a=party_a,
        party_b=party_b,
        effective_date="January 15, 2025",
        jurisdiction=USState.CALIFORNIA,
        confidentiality_period=3,
        custom_clauses=[
            "Non-Circumvention: Neither party shall circumvent the other to engage directly with disclosed contacts."
        ],
        additional_terms={
            "purpose": "evaluation of potential business partnership and technology collaboration"
        }
    )

    nda_doc = generator.generate_document(nda_params, use_ai_enhancement=True)

    print(f"\n✅ NDA Generated!")
    print(f"   Document ID: {nda_doc.document_id}")
    print(f"   Compliance Status: {nda_doc.compliance_status.value}")
    print(f"   Issues Found: {len(nda_doc.compliance_issues)}")

    if nda_doc.compliance_issues:
        print("\n   Compliance Issues:")
        for issue in nda_doc.compliance_issues[:3]:  # Show first 3
            print(f"   - [{issue.severity}] {issue.description}")

    # Show excerpt
    print("\n   Document Excerpt:")
    print("   " + "-" * 76)
    excerpt_lines = nda_doc.content.split('\n')[:15]
    for line in excerpt_lines:
        print(f"   {line}")
    print("   ...")

    print("\n📄 Generating Service Agreement...")

    # Generate Service Agreement
    service_params = DocumentParameters(
        document_type=DocumentType.SERVICE_AGREEMENT,
        party_a=party_b,  # Innovation Labs as provider
        party_b=party_a,  # TechCorp as client
        effective_date="February 1, 2025",
        jurisdiction=USState.TEXAS,
        compensation="$15,000 per month",
        termination_notice_days=30,
        additional_terms={
            "services": "Software development, quality assurance, and technical consulting services",
            "payment_terms": "Monthly invoicing, payment due within 15 days of invoice date",
            "ip_clause": "All intellectual property created during service provision becomes exclusive property of Client"
        }
    )

    service_doc = generator.generate_document(service_params, use_ai_enhancement=False)

    print(f"\n✅ Service Agreement Generated!")
    print(f"   Document ID: {service_doc.document_id}")
    print(f"   Compliance Status: {service_doc.compliance_status.value}")

    # Prepare for e-signature
    print("\n✍️  Preparing for E-Signature...")
    esig_info = generator.prepare_for_signature(service_doc.document_id)
    print(f"   Signers: {len(esig_info['signers'])}")
    for signer in esig_info['signers']:
        print(f"   - {signer['name']} ({signer['role']}): {signer['email']}")

    # Show analytics
    print("\n" + "=" * 80)
    print("Analytics Dashboard")
    print("=" * 80)
    analytics = generator.get_analytics()
    print(json.dumps(analytics, indent=2))

    # Export document
    print("\n" + "=" * 80)
    print("Document Export")
    print("=" * 80)
    export_path = f"/tmp/{nda_doc.document_id}.txt"
    with open(export_path, 'w') as f:
        f.write(generator.export_document(nda_doc.document_id, format="txt"))
    print(f"✅ Document exported to: {export_path}")

    print("\n" + "=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    demo_legal_generator()
