#!/usr/bin/env python3
"""
AI Project Manager Module
Intelligent Task Breakdown, Team Assignment & Timeline Prediction
Powered by Claude AI
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
import uuid


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task status states"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectStatus(Enum):
    """Project status states"""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ResourceType(Enum):
    """Resource types"""
    DEVELOPER = "developer"
    DESIGNER = "designer"
    QA = "qa"
    PROJECT_MANAGER = "project_manager"
    DEVOPS = "devops"
    DATA_SCIENTIST = "data_scientist"
    MARKETING = "marketing"
    SALES = "sales"


@dataclass
class TeamMember:
    """Represents a team member"""
    id: str
    name: str
    email: str
    role: ResourceType
    skills: List[str]
    availability: float  # 0.0 to 1.0 (percentage)
    hourly_rate: Optional[float] = None
    current_tasks: List[str] = field(default_factory=list)


@dataclass
class Task:
    """Represents a project task"""
    id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    estimated_hours: float
    actual_hours: float
    assigned_to: Optional[str]  # TeamMember ID
    dependencies: List[str]  # Task IDs
    tags: List[str]
    created_at: datetime
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    parent_task_id: Optional[str]
    subtasks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Project:
    """Represents a project"""
    id: str
    name: str
    description: str
    goals: List[str]
    status: ProjectStatus
    owner: str
    team_members: List[str]  # TeamMember IDs
    tasks: List[str]  # Task IDs
    start_date: datetime
    target_end_date: datetime
    predicted_end_date: Optional[datetime]
    budget: Optional[float]
    actual_cost: float
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceAllocation:
    """Represents resource allocation to a task"""
    task_id: str
    team_member_id: str
    allocated_hours: float
    allocation_percentage: float
    start_date: datetime
    end_date: datetime
    confidence_score: float  # AI confidence in assignment (0-1)


class TaskBreakdownEngine:
    """AI-powered task breakdown engine"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def breakdown_goal(self, goal: str, context: Optional[str] = None) -> List[Dict[str, Any]]:
        """Break down high-level goal into actionable tasks"""

        breakdown_prompt = f"""As an expert project manager, break down this project goal into specific, actionable tasks.

Goal: {goal}

{f'Context: {context}' if context else ''}

For each task, provide:
1. Title (concise, action-oriented)
2. Description (what needs to be done)
3. Estimated hours (realistic time estimate)
4. Priority (low, medium, high, critical)
5. Dependencies (which tasks must be completed first)
6. Required skills (what expertise is needed)
7. Subtasks (if the task is complex, break it down further)

Provide the breakdown as a JSON array of tasks:
[
  {{
    "title": "Task title",
    "description": "Detailed description",
    "estimated_hours": 8,
    "priority": "high",
    "dependencies": [],
    "required_skills": ["skill1", "skill2"],
    "subtasks": []
  }}
]

Focus on:
- Logical sequencing
- Realistic time estimates
- Clear dependencies
- Appropriate granularity (not too broad, not too detailed)
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": breakdown_prompt
                }]
            )

            result = response.content[0].text

            # Extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                tasks = json.loads(json_match.group())
                return tasks
            else:
                # Fallback
                return [{
                    "title": "Review and plan project",
                    "description": goal,
                    "estimated_hours": 4,
                    "priority": "high",
                    "dependencies": [],
                    "required_skills": ["planning"],
                    "subtasks": []
                }]

        except Exception as e:
            print(f"Task breakdown error: {e}")
            return [{
                "title": "Review and plan project",
                "description": goal,
                "estimated_hours": 4,
                "priority": "high",
                "dependencies": [],
                "required_skills": ["planning"],
                "subtasks": []
            }]


class TeamAssignmentOptimizer:
    """Optimizes team member assignment to tasks"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def optimize_assignments(
        self,
        tasks: List[Task],
        team_members: List[TeamMember]
    ) -> List[ResourceAllocation]:
        """Optimize task assignments based on skills, availability, and workload"""

        allocations = []

        # Create skill matrix
        for task in tasks:
            if task.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
                continue

            required_skills = task.metadata.get('required_skills', [])

            # Score each team member for this task
            best_match = None
            best_score = -1

            for member in team_members:
                score = self._calculate_assignment_score(task, member, required_skills)

                if score > best_score and member.availability > 0.2:
                    best_score = score
                    best_match = member

            if best_match:
                # Calculate allocation
                allocation = ResourceAllocation(
                    task_id=task.id,
                    team_member_id=best_match.id,
                    allocated_hours=task.estimated_hours,
                    allocation_percentage=min(task.estimated_hours / 40, best_match.availability),
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(hours=task.estimated_hours),
                    confidence_score=best_score
                )
                allocations.append(allocation)

        return allocations

    def _calculate_assignment_score(
        self,
        task: Task,
        member: TeamMember,
        required_skills: List[str]
    ) -> float:
        """Calculate how well a team member matches a task"""

        score = 0.0

        # Skill match (40% weight)
        if required_skills:
            skill_overlap = len(set(required_skills) & set(member.skills))
            skill_score = skill_overlap / len(required_skills)
            score += skill_score * 0.4

        # Availability (30% weight)
        score += member.availability * 0.3

        # Current workload (20% weight) - prefer less loaded members
        workload_score = max(0, 1.0 - (len(member.current_tasks) / 10))
        score += workload_score * 0.2

        # Priority matching (10% weight)
        if task.priority == TaskPriority.CRITICAL:
            score += 0.1

        return score


class TimelinePredictor:
    """Predicts project timelines using AI"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def predict_timeline(
        self,
        project: Project,
        tasks: List[Task],
        team_members: List[TeamMember]
    ) -> Tuple[datetime, Dict[str, Any]]:
        """Predict project completion date and provide insights"""

        # Calculate critical path
        total_hours = sum(task.estimated_hours for task in tasks)
        available_capacity = sum(member.availability * 40 for member in team_members)  # hours per week

        if available_capacity > 0:
            weeks_needed = total_hours / available_capacity
            predicted_date = datetime.now() + timedelta(weeks=weeks_needed)
        else:
            predicted_date = datetime.now() + timedelta(weeks=52)  # Default to 1 year

        # Calculate risk factors
        risk_factors = self._analyze_risks(project, tasks, team_members)

        # Add buffer based on complexity and risk
        risk_buffer = risk_factors['overall_risk'] * 0.3  # 30% buffer for high risk
        buffered_weeks = weeks_needed * (1 + risk_buffer)
        final_predicted_date = datetime.now() + timedelta(weeks=buffered_weeks)

        insights = {
            "predicted_completion": final_predicted_date.isoformat(),
            "estimated_hours": total_hours,
            "available_capacity": available_capacity,
            "weeks_needed": weeks_needed,
            "risk_adjusted_weeks": buffered_weeks,
            "risk_factors": risk_factors,
            "confidence": 1.0 - risk_factors['overall_risk'],
            "critical_path": self._find_critical_path(tasks),
            "bottlenecks": self._identify_bottlenecks(tasks, team_members)
        }

        return final_predicted_date, insights

    def _analyze_risks(
        self,
        project: Project,
        tasks: List[Task],
        team_members: List[TeamMember]
    ) -> Dict[str, Any]:
        """Analyze project risks"""

        risks = {
            "team_capacity": 0.0,
            "task_complexity": 0.0,
            "dependency_risk": 0.0,
            "resource_risk": 0.0,
            "overall_risk": 0.0
        }

        # Team capacity risk
        avg_availability = sum(m.availability for m in team_members) / len(team_members) if team_members else 0
        risks["team_capacity"] = 1.0 - avg_availability

        # Task complexity risk
        avg_task_hours = sum(t.estimated_hours for t in tasks) / len(tasks) if tasks else 0
        risks["task_complexity"] = min(avg_task_hours / 40, 1.0)  # Normalize to 40 hours

        # Dependency risk
        avg_dependencies = sum(len(t.dependencies) for t in tasks) / len(tasks) if tasks else 0
        risks["dependency_risk"] = min(avg_dependencies / 5, 1.0)  # Normalize to 5 deps

        # Resource risk (skills mismatch)
        all_required_skills = set()
        for task in tasks:
            all_required_skills.update(task.metadata.get('required_skills', []))

        all_team_skills = set()
        for member in team_members:
            all_team_skills.update(member.skills)

        if all_required_skills:
            skill_coverage = len(all_team_skills & all_required_skills) / len(all_required_skills)
            risks["resource_risk"] = 1.0 - skill_coverage
        else:
            risks["resource_risk"] = 0.0

        # Overall risk
        risks["overall_risk"] = (
            risks["team_capacity"] * 0.3 +
            risks["task_complexity"] * 0.2 +
            risks["dependency_risk"] * 0.3 +
            risks["resource_risk"] * 0.2
        )

        return risks

    def _find_critical_path(self, tasks: List[Task]) -> List[str]:
        """Find critical path through task dependencies"""
        # Simplified critical path - longest dependency chain
        max_chain = []

        def find_chain(task_id: str, visited: set) -> List[str]:
            if task_id in visited:
                return []

            visited.add(task_id)
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                return []

            if not task.dependencies:
                return [task_id]

            longest = []
            for dep_id in task.dependencies:
                chain = find_chain(dep_id, visited.copy())
                if len(chain) > len(longest):
                    longest = chain

            return longest + [task_id]

        for task in tasks:
            chain = find_chain(task.id, set())
            if len(chain) > len(max_chain):
                max_chain = chain

        return max_chain

    def _identify_bottlenecks(
        self,
        tasks: List[Task],
        team_members: List[TeamMember]
    ) -> List[Dict[str, Any]]:
        """Identify potential bottlenecks"""
        bottlenecks = []

        # Over-allocated team members
        for member in team_members:
            if len(member.current_tasks) > 5:
                bottlenecks.append({
                    "type": "resource_overallocation",
                    "resource": member.name,
                    "severity": "high",
                    "description": f"{member.name} has {len(member.current_tasks)} tasks assigned"
                })

        # Tasks with many dependencies
        for task in tasks:
            if len(task.dependencies) > 3:
                bottlenecks.append({
                    "type": "dependency_bottleneck",
                    "task": task.title,
                    "severity": "medium",
                    "description": f"Task has {len(task.dependencies)} dependencies"
                })

        return bottlenecks


class AIProjectManager:
    """Main AI Project Manager class"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI Project Manager"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.task_breakdown = TaskBreakdownEngine(self.api_key)
        self.team_optimizer = TeamAssignmentOptimizer(self.api_key)
        self.timeline_predictor = TimelinePredictor(self.api_key)

        # Storage
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.team_members: Dict[str, TeamMember] = {}
        self.allocations: List[ResourceAllocation] = []

    def create_project(
        self,
        name: str,
        description: str,
        goals: List[str],
        owner: str,
        target_end_date: datetime,
        budget: Optional[float] = None
    ) -> Project:
        """Create a new project"""

        project_id = str(uuid.uuid4())

        project = Project(
            id=project_id,
            name=name,
            description=description,
            goals=goals,
            status=ProjectStatus.PLANNING,
            owner=owner,
            team_members=[],
            tasks=[],
            start_date=datetime.now(),
            target_end_date=target_end_date,
            predicted_end_date=None,
            budget=budget,
            actual_cost=0.0,
            created_at=datetime.now()
        )

        self.projects[project_id] = project
        return project

    def add_team_member(
        self,
        name: str,
        email: str,
        role: ResourceType,
        skills: List[str],
        availability: float = 1.0,
        hourly_rate: Optional[float] = None
    ) -> TeamMember:
        """Add a team member"""

        member_id = str(uuid.uuid4())

        member = TeamMember(
            id=member_id,
            name=name,
            email=email,
            role=role,
            skills=skills,
            availability=availability,
            hourly_rate=hourly_rate,
            current_tasks=[]
        )

        self.team_members[member_id] = member
        return member

    def breakdown_project(self, project_id: str) -> List[Task]:
        """Break down project goals into tasks using AI"""

        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")

        project = self.projects[project_id]

        all_tasks = []

        # Break down each goal
        for goal in project.goals:
            task_data = self.task_breakdown.breakdown_goal(
                goal,
                context=project.description
            )

            # Convert to Task objects
            for td in task_data:
                task_id = str(uuid.uuid4())

                priority_map = {
                    "low": TaskPriority.LOW,
                    "medium": TaskPriority.MEDIUM,
                    "high": TaskPriority.HIGH,
                    "critical": TaskPriority.CRITICAL
                }

                task = Task(
                    id=task_id,
                    title=td.get("title", "Untitled Task"),
                    description=td.get("description", ""),
                    priority=priority_map.get(td.get("priority", "medium").lower(), TaskPriority.MEDIUM),
                    status=TaskStatus.NOT_STARTED,
                    estimated_hours=float(td.get("estimated_hours", 4)),
                    actual_hours=0.0,
                    assigned_to=None,
                    dependencies=[],
                    tags=td.get("required_skills", []),
                    created_at=datetime.now(),
                    due_date=None,
                    completed_at=None,
                    parent_task_id=None,
                    metadata={
                        "required_skills": td.get("required_skills", []),
                        "goal": goal
                    }
                )

                self.tasks[task_id] = task
                all_tasks.append(task)
                project.tasks.append(task_id)

        return all_tasks

    def assign_resources(self, project_id: str) -> List[ResourceAllocation]:
        """Automatically assign team members to tasks"""

        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")

        project = self.projects[project_id]

        # Get project tasks
        project_tasks = [self.tasks[tid] for tid in project.tasks if tid in self.tasks]

        # Get project team members
        project_team = [self.team_members[mid] for mid in project.team_members if mid in self.team_members]

        if not project_team:
            # Use all team members if none assigned
            project_team = list(self.team_members.values())

        # Optimize assignments
        allocations = self.team_optimizer.optimize_assignments(project_tasks, project_team)

        # Apply assignments
        for allocation in allocations:
            if allocation.task_id in self.tasks:
                task = self.tasks[allocation.task_id]
                task.assigned_to = allocation.team_member_id

                # Update team member
                if allocation.team_member_id in self.team_members:
                    member = self.team_members[allocation.team_member_id]
                    member.current_tasks.append(allocation.task_id)

        self.allocations.extend(allocations)
        return allocations

    def predict_timeline(self, project_id: str) -> Dict[str, Any]:
        """Predict project timeline and provide insights"""

        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")

        project = self.projects[project_id]

        # Get project tasks and team
        project_tasks = [self.tasks[tid] for tid in project.tasks if tid in self.tasks]
        project_team = [self.team_members[mid] for mid in project.team_members if mid in self.team_members]

        if not project_team:
            project_team = list(self.team_members.values())

        # Predict
        predicted_date, insights = self.timeline_predictor.predict_timeline(
            project,
            project_tasks,
            project_team
        )

        # Update project
        project.predicted_end_date = predicted_date

        return insights

    def update_task_status(self, task_id: str, status: TaskStatus, actual_hours: Optional[float] = None):
        """Update task status"""

        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        task.status = status

        if actual_hours is not None:
            task.actual_hours = actual_hours

        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now()

    def get_project_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get comprehensive project dashboard"""

        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")

        project = self.projects[project_id]
        project_tasks = [self.tasks[tid] for tid in project.tasks if tid in self.tasks]

        # Calculate metrics
        total_tasks = len(project_tasks)
        completed_tasks = sum(1 for t in project_tasks if t.status == TaskStatus.COMPLETED)
        in_progress_tasks = sum(1 for t in project_tasks if t.status == TaskStatus.IN_PROGRESS)
        blocked_tasks = sum(1 for t in project_tasks if t.status == TaskStatus.BLOCKED)

        total_estimated_hours = sum(t.estimated_hours for t in project_tasks)
        total_actual_hours = sum(t.actual_hours for t in project_tasks)

        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Status distribution
        status_dist = {}
        for task in project_tasks:
            status = task.status.value
            status_dist[status] = status_dist.get(status, 0) + 1

        # Team workload
        team_workload = {}
        for member_id in project.team_members:
            if member_id in self.team_members:
                member = self.team_members[member_id]
                assigned_hours = sum(
                    self.tasks[tid].estimated_hours
                    for tid in member.current_tasks
                    if tid in self.tasks
                )
                team_workload[member.name] = {
                    "assigned_tasks": len(member.current_tasks),
                    "assigned_hours": assigned_hours,
                    "availability": member.availability
                }

        return {
            "project_id": project_id,
            "project_name": project.name,
            "status": project.status.value,
            "completion_percentage": completion_percentage,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "blocked_tasks": blocked_tasks,
            "status_distribution": status_dist,
            "total_estimated_hours": total_estimated_hours,
            "total_actual_hours": total_actual_hours,
            "hours_variance": total_actual_hours - total_estimated_hours,
            "team_workload": team_workload,
            "start_date": project.start_date.isoformat(),
            "target_end_date": project.target_end_date.isoformat(),
            "predicted_end_date": project.predicted_end_date.isoformat() if project.predicted_end_date else None,
            "budget": project.budget,
            "actual_cost": project.actual_cost,
            "budget_variance": project.actual_cost - project.budget if project.budget else 0
        }

    def get_analytics(self) -> Dict[str, Any]:
        """Get overall analytics"""

        return {
            "total_projects": len(self.projects),
            "total_tasks": len(self.tasks),
            "total_team_members": len(self.team_members),
            "active_projects": sum(1 for p in self.projects.values() if p.status == ProjectStatus.ACTIVE),
            "total_allocations": len(self.allocations),
            "average_team_utilization": sum(m.availability for m in self.team_members.values()) / len(self.team_members) if self.team_members else 0
        }


# Integration with external systems
class JiraIntegration:
    """Integration with Jira"""

    def __init__(self, jira_url: str, api_token: str):
        self.jira_url = jira_url
        self.api_token = api_token

    def sync_tasks(self, project_manager: AIProjectManager, project_id: str):
        """Sync tasks to Jira (mock implementation)"""
        print(f"Syncing tasks to Jira for project {project_id}")
        # In production, implement actual Jira API calls
        return {"status": "success", "synced_tasks": 0}


class AsanaIntegration:
    """Integration with Asana"""

    def __init__(self, api_token: str):
        self.api_token = api_token

    def sync_tasks(self, project_manager: AIProjectManager, project_id: str):
        """Sync tasks to Asana (mock implementation)"""
        print(f"Syncing tasks to Asana for project {project_id}")
        return {"status": "success", "synced_tasks": 0}


def demo_project_manager():
    """Demo function showing AI Project Manager capabilities"""
    print("=" * 80)
    print("AI Project Manager - Demo")
    print("=" * 80)

    # Initialize
    try:
        pm = AIProjectManager()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Create project
    print("\n📊 Creating Project...")
    project = pm.create_project(
        name="E-Commerce Platform Redesign",
        description="Complete redesign of e-commerce platform with modern UI/UX and enhanced features",
        goals=[
            "Design and implement new user interface with React",
            "Migrate backend to microservices architecture",
            "Implement advanced search and filtering",
            "Add AI-powered product recommendations",
            "Optimize for mobile and improve performance"
        ],
        owner="product@company.com",
        target_end_date=datetime.now() + timedelta(days=90),
        budget=150000.0
    )

    print(f"✅ Project Created: {project.name}")
    print(f"   ID: {project.id}")
    print(f"   Goals: {len(project.goals)}")

    # Add team members
    print("\n👥 Adding Team Members...")

    members = [
        pm.add_team_member("Alice Johnson", "alice@company.com", ResourceType.DEVELOPER,
                          ["React", "TypeScript", "Frontend"], availability=0.8, hourly_rate=100),
        pm.add_team_member("Bob Smith", "bob@company.com", ResourceType.DEVELOPER,
                          ["Python", "Django", "Backend", "Microservices"], availability=1.0, hourly_rate=95),
        pm.add_team_member("Carol White", "carol@company.com", ResourceType.DESIGNER,
                          ["UI/UX", "Figma", "User Research"], availability=0.6, hourly_rate=85),
        pm.add_team_member("Dave Brown", "dave@company.com", ResourceType.QA,
                          ["Testing", "Automation", "Selenium"], availability=1.0, hourly_rate=75),
        pm.add_team_member("Eve Davis", "eve@company.com", ResourceType.DEVOPS,
                          ["Docker", "Kubernetes", "AWS", "CI/CD"], availability=0.5, hourly_rate=110),
    ]

    # Add team to project
    for member in members:
        project.team_members.append(member.id)

    print(f"✅ Added {len(members)} team members")

    # Break down project into tasks
    print("\n🤖 AI Breaking Down Project Goals into Tasks...")
    tasks = pm.breakdown_project(project.id)

    print(f"✅ Generated {len(tasks)} tasks")
    print("\nSample Tasks:")
    for i, task in enumerate(tasks[:5], 1):
        print(f"   {i}. [{task.priority.name}] {task.title}")
        print(f"      Estimated: {task.estimated_hours}h | Skills: {', '.join(task.tags[:3])}")

    # Assign resources
    print("\n🎯 Optimizing Team Assignments...")
    allocations = pm.assign_resources(project.id)

    print(f"✅ Created {len(allocations)} resource allocations")
    print("\nSample Assignments:")
    for allocation in allocations[:5]:
        task = pm.tasks[allocation.task_id]
        member = pm.team_members[allocation.team_member_id]
        print(f"   • {task.title[:50]}...")
        print(f"     → Assigned to: {member.name} ({member.role.value})")
        print(f"     → Confidence: {allocation.confidence_score:.2f}")

    # Predict timeline
    print("\n📅 Predicting Project Timeline...")
    insights = pm.predict_timeline(project.id)

    print(f"✅ Timeline Predicted")
    print(f"\n   Predicted Completion: {insights['predicted_completion'][:10]}")
    print(f"   Total Hours: {insights['estimated_hours']:.0f}h")
    print(f"   Team Capacity: {insights['available_capacity']:.0f}h/week")
    print(f"   Estimated Duration: {insights['weeks_needed']:.1f} weeks")
    print(f"   Risk-Adjusted Duration: {insights['risk_adjusted_weeks']:.1f} weeks")
    print(f"   Confidence: {insights['confidence']:.0%}")

    print("\n   Risk Factors:")
    for risk_type, risk_value in insights['risk_factors'].items():
        if risk_type != 'overall_risk':
            print(f"   - {risk_type.replace('_', ' ').title()}: {risk_value:.0%}")

    if insights.get('bottlenecks'):
        print("\n   ⚠️  Bottlenecks Identified:")
        for bottleneck in insights['bottlenecks'][:3]:
            print(f"   - [{bottleneck['severity']}] {bottleneck['description']}")

    # Get project dashboard
    print("\n" + "=" * 80)
    print("Project Dashboard")
    print("=" * 80)

    dashboard = pm.get_project_dashboard(project.id)
    print(json.dumps(dashboard, indent=2))

    # Get analytics
    print("\n" + "=" * 80)
    print("Analytics")
    print("=" * 80)
    analytics = pm.get_analytics()
    print(json.dumps(analytics, indent=2))

    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    demo_project_manager()
