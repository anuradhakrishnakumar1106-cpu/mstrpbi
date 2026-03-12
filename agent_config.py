"""
BI Migration Agent Configuration
MicroStrategy to Power BI Migration Workflow

This module configures the AI agent for orchestrating complex BI migrations
with controlled, deterministic behavior suitable for enterprise transformations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

# ============================================================================
# AI ENGINE SELECTION
# ============================================================================

class AIEngine(Enum):
    """Supported AI engine providers"""
    AZURE_OPENAI = "AzureOpenAI"
    GOOGLE_AI = "GoogleAI"
    AMAZON_BEDROCK = "AmazonBedrock"


class ModelEngine(Enum):
    """Supported model engines"""
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"


# ============================================================================
# AGENT CONFIGURATION DATACLASS
# ============================================================================

@dataclass
class BehaviorPreset:
    """Behavior configuration for the agent"""
    
    # Temperature: Controls randomness/creativity
    # 0.0-0.5: Deterministic, good for technical accuracy
    # 0.5-1.0: Creative, good for brainstorming
    # CHOSEN: 0.3 for consistent, reliable migration logic
    temperature: float = 0.3
    
    # Top P: Nucleus sampling parameter
    # 0.0-0.5: Focused, consistent responses
    # 0.5-1.0: More diverse responses
    # CHOSEN: 0.9 for balanced exploration with safety
    top_p: float = 0.9
    
    # Max iterations: Maximum conversation/loop iterations
    # CHOSEN: 10 for iterative refinement without infinite loops
    max_iterations: int = 10
    
    # Max RPM: Requests per minute rate limit
    # Prevents API rate limiting and cost explosion
    # CHOSEN: 60 RPM = 1 request per second average
    max_rpm: int = 60
    
    # Max execution time in seconds
    # CHOSEN: 300 seconds (5 minutes) per task
    # Prevents long-running operations from blocking
    max_execution_time_sec: int = 300
    
    # Additional parameters for fine-tuning
    frequency_penalty: float = 0.0  # Decreases likelihood of repeating tokens
    presence_penalty: float = 0.0   # Decreases likelihood of new topics


@dataclass
class AgentConfig:
    """Complete agent configuration"""
    
    # Agent Identity
    agent_name: str = "MicroStrategy-to-PowerBI Migration Architect"
    agent_version: str = "1.0.0"
    agent_description: str = """
        Intelligent BI migration coordinator specializing in MicroStrategy to Power BI transformations.
        Manages assessment, design, development, testing, and cutover of enterprise BI migrations.
    """
    
    # AI Engine Configuration
    ai_engine: AIEngine = AIEngine.AZURE_OPENAI
    model_engine: ModelEngine = ModelEngine.GPT_4O
    
    # Azure OpenAI specific settings
    azure_endpoint: str = "${AZURE_OPENAI_ENDPOINT}"  # Set from environment
    azure_api_key: str = "${AZURE_OPENAI_KEY}"         # Set from environment
    azure_api_version: str = "2024-02-15-preview"
    azure_deployment_name: str = "gpt-4o-migration-agent"
    
    # Behavior configuration
    behavior: BehaviorPreset = None
    
    # Context window configuration
    max_tokens_per_request: int = 8192
    max_tokens_per_response: int = 4096
    
    # Retry configuration
    max_retries: int = 3
    retry_delay_sec: float = 2.0
    
    # Tool configuration
    enable_tools: List[str] = field(default_factory=lambda: [
        "mstr_object_analyzer",
        "dax_formula_generator",
        "transformation_validator",
        "security_model_mapper",
        "migration_report_generator",
        "model_performance_analyzer"
    ])
    
    def __post_init__(self):
        """Set defaults if not provided"""
        if self.behavior is None:
            self.behavior = BehaviorPreset()


# ============================================================================
# INSTANTIATE AGENT CONFIGURATION
# ============================================================================

AGENT_CONFIG = AgentConfig()

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

@dataclass
class ToolDefinition:
    """Schema for tool definitions"""
    tool_id: str
    tool_name: str
    description: str
    category: str
    input_schema: Dict
    output_schema: Dict
    timeout_sec: int = 120
    requires_authentication: bool = False
    async_support: bool = True


# Tool 1: MicroStrategy Object Analyzer
TOOL_MSTR_ANALYZER = ToolDefinition(
    tool_id="mstr_object_analyzer",
    tool_name="MicroStrategy Object Analyzer",
    description="Parses and analyzes MicroStrategy objects to understand structure and migration complexity",
    category="Analysis",
    input_schema={
        "type": "object",
        "properties": {
            "object_name": {"type": "string"},
            "object_type": {"type": "string", "enum": ["report", "metric", "hierarchy", "filter"]},
            "definition_content": {"type": "string"},
            "environment_context": {"type": "object"}
        },
        "required": ["object_name", "object_type", "definition_content"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "complexity_score": {"type": "integer", "minimum": 0, "maximum": 100},
            "migration_effort": {"type": "string", "enum": ["Low", "Medium", "High", "Very High"]},
            "dependencies": {"type": "array"},
            "power_bi_equivalent": {"type": "object"}
        }
    },
    timeout_sec=120,
    requires_authentication=True,
    async_support=True
)

# Tool 2: DAX Formula Generator
TOOL_DAX_GENERATOR = ToolDefinition(
    tool_id="dax_formula_generator",
    tool_name="DAX Formula Generator",
    description="Converts MicroStrategy metrics into Power BI DAX measures",
    category="Code Generation",
    input_schema={
        "type": "object",
        "properties": {
            "metric_definition": {"type": "string"},
            "context": {"type": "object"},
            "parameters": {"type": "object"}
        },
        "required": ["metric_definition", "context"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "dax_formula": {"type": "string"},
            "supporting_measures": {"type": "array"},
            "performance_assessment": {"type": "object"},
            "documentation": {"type": "object"}
        }
    },
    timeout_sec=60,
    requires_authentication=False,
    async_support=True
)

# Tool 3: Transformation Validator
TOOL_TRANSFORM_VALIDATOR = ToolDefinition(
    tool_id="transformation_validator",
    tool_name="Transformation Validator",
    description="Compares MicroStrategy vs Power BI results to validate migration accuracy",
    category="Quality Assurance",
    input_schema={
        "type": "object",
        "properties": {
            "validation_type": {"type": "string"},
            "mstr_query_result": {"type": "object"},
            "powerbi_query_result": {"type": "object"},
            "validation_rules": {"type": "object"}
        },
        "required": ["validation_type", "mstr_query_result", "powerbi_query_result"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "overall_status": {"type": "string", "enum": ["PASS", "FAIL", "PARTIAL"]},
            "match_percentage": {"type": "number"},
            "discrepancy_details": {"type": "array"},
            "root_cause_analysis": {"type": "array"}
        }
    },
    timeout_sec=300,
    requires_authentication=True,
    async_support=True
)

# Tool 4: Security Model Mapper
TOOL_SECURITY_MAPPER = ToolDefinition(
    tool_id="security_model_mapper",
    tool_name="Security Model Mapper",
    description="Translates MicroStrategy security to Power BI RLS",
    category="Security & Compliance",
    input_schema={
        "type": "object",
        "properties": {
            "security_type": {"type": "string"},
            "security_definition": {"type": "string"},
            "user_structure": {"type": "object"},
            "target_model_context": {"type": "object"}
        },
        "required": ["security_type", "security_definition", "user_structure"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "rls_configurations": {"type": "array"},
            "user_mapping": {"type": "object"},
            "implementation_steps": {"type": "array"},
            "testing_plan": {"type": "object"}
        }
    },
    timeout_sec=30,
    requires_authentication=True,
    async_support=False
)

# Tool 5: Migration Report Generator
TOOL_REPORT_GENERATOR = ToolDefinition(
    tool_id="migration_report_generator",
    tool_name="Migration Report Generator",
    description="Creates comprehensive migration documentation",
    category="Reporting & Documentation",
    input_schema={
        "type": "object",
        "properties": {
            "report_type": {"type": "string"},
            "migration_data": {"type": "object"},
            "output_format": {"type": "string", "enum": ["markdown", "pdf", "html", "excel"]}
        },
        "required": ["report_type", "migration_data"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "report_id": {"type": "string"},
            "document": {"type": "object"},
            "metadata": {"type": "object"}
        }
    },
    timeout_sec=60,
    requires_authentication=False,
    async_support=True
)

# Tool 6: Model Performance Analyzer
TOOL_PERFORMANCE_ANALYZER = ToolDefinition(
    tool_id="model_performance_analyzer",
    tool_name="Model Performance Analyzer",
    description="Analyzes Power BI model performance and optimization recommendations",
    category="Performance & Optimization",
    input_schema={
        "type": "object",
        "properties": {
            "model_definition": {"type": "object"},
            "workload_characteristics": {"type": "object"}
        },
        "required": ["model_definition"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "overall_performance_score": {"type": "integer"},
            "bottleneck_analysis": {"type": "array"},
            "recommendations": {"type": "array"},
            "performance_benchmarks": {"type": "object"}
        }
    },
    timeout_sec=120,
    requires_authentication=True,
    async_support=True
)

# Registry of all tools
TOOLS = {
    "mstr_object_analyzer": TOOL_MSTR_ANALYZER,
    "dax_formula_generator": TOOL_DAX_GENERATOR,
    "transformation_validator": TOOL_TRANSFORM_VALIDATOR,
    "security_model_mapper": TOOL_SECURITY_MAPPER,
    "migration_report_generator": TOOL_REPORT_GENERATOR,
    "model_performance_analyzer": TOOL_PERFORMANCE_ANALYZER
}

# ============================================================================
# PHASE DEFINITIONS
# ============================================================================

@dataclass
class Phase:
    """Migration phase definition"""
    number: int
    name: str
    duration_days: int
    objectives: List[str]
    key_deliverables: List[str]
    success_criteria: List[str]


MIGRATION_PHASES = [
    Phase(
        number=1,
        name="Assessment & Planning",
        duration_days=3,
        objectives=[
            "Understand current MicroStrategy environment",
            "Document all reports, metrics, and data sources",
            "Assess risks and complexities",
            "Define migration strategy"
        ],
        key_deliverables=[
            "MicroStrategy Inventory",
            "Risk Assessment Report",
            "Migration Strategy Document",
            "Effort & Timeline Estimate"
        ],
        success_criteria=[
            "All objects catalogued and analyzed",
            "Risks identified with mitigation plans",
            "Timeline agreed with stakeholders",
            "Resources allocated"
        ]
    ),
    Phase(
        number=2,
        name="Design & Architecture",
        duration_days=4,
        objectives=[
            "Design Power BI semantic model",
            "Create measure conversion specifications",
            "Design RLS security model",
            "Plan data and refresh strategy"
        ],
        key_deliverables=[
            "Semantic Model Design Document",
            "Measure Mapping Specification",
            "RLS Design Document",
            "Data Flow Diagram"
        ],
        success_criteria=[
            "Design approved by data governance",
            "All metrics have DAX design",
            "Security requirements captured",
            "Performance assumptions documented"
        ]
    ),
    Phase(
        number=3,
        name="Development",
        duration_days=13,
        objectives=[
            "Build Power BI semantic model",
            "Implement all measures",
            "Create Power BI reports",
            "Implement RLS and security"
        ],
        key_deliverables=[
            "Power BI PBIX file",
            "All reports and dashboards",
            "Transformation mappings",
            "Validation results"
        ],
        success_criteria=[
            "100% measures implemented",
            "Variance <0.5% on financial metrics",
            "All reports recreated",
            "RLS implemented in staging"
        ]
    ),
    Phase(
        number=4,
        name="Testing & Optimization",
        duration_days=5,
        objectives=[
            "Conduct user acceptance testing",
            "Validate calculation accuracy",
            "Test security implementation",
            "Optimize performance"
        ],
        key_deliverables=[
            "Test Results Report",
            "Performance Benchmarks",
            "UAT Sign-off",
            "Optimization Changes Log"
        ],
        success_criteria=[
            "100% UAT tests passed",
            "Performance P90 <5 seconds",
            "Security validated with sample users",
            "Ready for production cutover"
        ]
    ),
    Phase(
        number=5,
        name="Cutover & Go-Live",
        duration_days=2,
        objectives=[
            "Execute controlled production cutover",
            "Validate production data",
            "Redirect users to Power BI",
            "Monitor for critical issues"
        ],
        key_deliverables=[
            "Cutover Plan and Checklist",
            "Cutover Execution Log",
            "Issue Resolution Log",
            "Success Criteria Validation"
        ],
        success_criteria=[
            "Final reconciliation completed",
            "All users transitioned successfully",
            "No critical issues in first 24 hours",
            "Rollback not required"
        ]
    ),
    Phase(
        number=6,
        name="Knowledge Transfer & Handoff",
        duration_days=3,
        objectives=[
            "Complete documentation",
            "Train support team",
            "Establish monitoring",
            "Prepare for decommissioning"
        ],
        key_deliverables=[
            "Technical Documentation",
            "Administrator Guide",
            "End-User Guide",
            "Lessons Learned Report"
        ],
        success_criteria=[
            "Documentation complete and reviewed",
            "Support team trained and certified",
            "Monitoring dashboards operational",
            "Decommission plan agreed"
        ]
    )
]

# ============================================================================
# SYSTEM PROMPTS
# ============================================================================

SYSTEM_PROMPT = """You are the MicroStrategy-to-PowerBI Migration Architect Agent, an expert AI system designed to 
orchestrate complex BI platform migrations for enterprise organizations.

CORE IDENTITY:
- You have 10+ years of experience in enterprise data warehouse migrations
- You have successfully migrated 50+ organizations to Power BI
- You understand both MicroStrategy's dimensional modeling and Power BI's DAX language
- You are compassionate about data accuracy and obsessive about maintaining business logic

OPERATIONAL PHILOSOPHY:
1. Validation over Speed: Never compromise data accuracy for schedule
2. Comprehensive Documentation: Every transformation decision is documented
3. Stakeholder Transparency: Clear communication of progress, risks, and decisions
4. Phased Approach: Avoid high-risk "Big Bang" migrations when possible
5. Change Control: All production changes follow formal processes

DECISION-MAKING PRINCIPLE:
When uncertain, escalate to human decision-makers. Your role is to provide analysis, recommendations, 
and implementation, but humans decide on trade-offs between scope, speed, and quality.

TOOLS AVAILABLE:
1. MicroStrategy Object Analyzer - Understand source environment
2. DAX Formula Generator - Create Power BI measures
3. Transformation Validator - Validate migration accuracy
4. Security Model Mapper - Translate security rules
5. Migration Report Generator - Document progress
6. Model Performance Analyzer - Optimize performance

USE THESE TOOLS proactively to complete assigned tasks."""

INITIAL_MESSAGE = """Welcome to the BI Migration Agent System. I'm the MicroStrategy-to-PowerBI Migration Architect.

I'm configured to guide your organization through a structured, validated migration with:
✓ AzureOpenAI GPT-4o as the AI engine
✓ Low temperature (0.3) for consistent, deterministic technical decisions
✓ Maximum 10 iterations per task to prevent infinite loops
✓ 5-minute timeout per task execution
✓ Full tool support for analysis, design, validation, and reporting

Current Configuration:
- AI Engine: AzureOpenAI
- Model: GPT-4o
- Temperature: 0.3 (deterministic)
- Top P: 0.9 (focused but balanced)
- Max RPM: 60 (quality control)
- Max Execution Time: 300 seconds

I'm ready to help with:
1. ASSESS your MicroStrategy environment
2. DESIGN your Power BI semantic model
3. DEVELOP measures and reports
4. TEST and validate migrations
5. PLAN and execute production cutover
6. DOCUMENT and transfer knowledge

What would you like to start with?"""

# ============================================================================
# CONFIGURATION DISPLAY
# ============================================================================

def print_config():
    """Print agent configuration for verification"""
    print("=" * 80)
    print("BI MIGRATION AGENT - CONFIGURATION SUMMARY")
    print("=" * 80)
    
    print(f"\nAgent Name: {AGENT_CONFIG.agent_name}")
    print(f"Version: {AGENT_CONFIG.agent_version}")
    
    print(f"\nAI ENGINE: {AGENT_CONFIG.ai_engine.value}")
    print(f"Model: {AGENT_CONFIG.model_engine.value}")
    
    print("\nBEHAVIOR PRESET:")
    print(f"  - Temperature: {AGENT_CONFIG.behavior.temperature}")
    print(f"  - Top P: {AGENT_CONFIG.behavior.top_p}")
    print(f"  - Max Iterations: {AGENT_CONFIG.behavior.max_iterations}")
    print(f"  - Max RPM: {AGENT_CONFIG.behavior.max_rpm}")
    print(f"  - Max Execution Time: {AGENT_CONFIG.behavior.max_execution_time_sec} seconds")
    
    print(f"\nTOOLS ENABLED: {len(AGENT_CONFIG.enable_tools)}")
    for tool in AGENT_CONFIG.enable_tools:
        print(f"  ✓ {tool}")
    
    print(f"\nMIGRATION PHASES: {len(MIGRATION_PHASES)}")
    for phase in MIGRATION_PHASES:
        print(f"  {phase.number}. {phase.name} ({phase.duration_days} days)")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_config()
    print(f"\n{INITIAL_MESSAGE}")
