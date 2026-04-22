# pipelines/plan_generator.py
"""
PlanGenerator -- Phase 1 + Phase 2 Upgrade

Generates a structured 4-week personalized learning plan based on:
  - Top skills extracted from the job market
  - Target role type
  - User skill level (beginner / intermediate / advanced)
  - [Phase 2] Resume skill gap analysis (gap_skills prioritized Week 1/2)

Gap-aware logic:
  - If gap_skills are provided, HIGH-priority gaps fill Weeks 1-2 first
  - MEDIUM-priority gaps fill Week 3
  - Remaining market skills fill Week 4
  - Matched/known skills are SKIPPED (user already has them)

Phase 4+: Will be converted into a PlanningAgent.
"""

from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_taxonomy import ROLE_FOCUS, SKILL_TAXONOMY, LEARNING_RESOURCES


# Learning time estimates per skill (hours/week)
SKILL_DIFFICULTY = {
    "beginner":     {"hours_per_skill": 3,   "max_skills_per_week": 2},
    "intermediate": {"hours_per_skill": 2,   "max_skills_per_week": 3},
    "advanced":     {"hours_per_skill": 1.5, "max_skills_per_week": 4}
}

WEEK_THEMES = [
    "Foundation Sprint -- Critical Skill Gaps",
    "Deep Dive -- Role-Critical Tools",
    "Hands-On Projects -- Build & Deploy",
    "Advanced Topics & Portfolio Showcase"
]

WEEK_THEMES_GENERIC = [
    "Foundation Sprint -- Core Skills",
    "Deep Dive -- Role-Critical Tools",
    "Hands-On Projects -- Build & Deploy",
    "Advanced Topics & Portfolio Showcase"
]


class WeeklyTask:
    """A single learning task within a week."""

    def __init__(self, skill: str, category: str, hours: float,
                 resource_url: str, platform: str, priority: str,
                 is_gap: bool = False):
        self.skill = skill
        self.category = category
        self.hours = hours
        self.resource_url = resource_url
        self.platform = platform
        self.priority = priority   # HIGH / MEDIUM / LOW
        self.is_gap = is_gap       # True = from resume gap analysis

    def to_dict(self) -> Dict:
        return {
            "skill": self.skill,
            "category": self.category,
            "hours": self.hours,
            "resource_url": self.resource_url,
            "platform": self.platform,
            "priority": self.priority,
            "is_gap": self.is_gap
        }


class WeekPlan:
    """A single week's learning plan."""

    def __init__(self, week_number: int, theme: str, start_date: str):
        self.week_number = week_number
        self.theme = theme
        self.start_date = start_date
        self.tasks: List[WeeklyTask] = []
        self.total_hours: float = 0.0

    def add_task(self, task: WeeklyTask):
        self.tasks.append(task)
        self.total_hours += task.hours

    def to_dict(self) -> Dict:
        return {
            "week_number": self.week_number,
            "theme": self.theme,
            "start_date": self.start_date,
            "total_hours": round(self.total_hours, 1),
            "tasks": [t.to_dict() for t in self.tasks]
        }


class PlanGenerator:
    """
    Generates a 4-week adaptive learning plan.

    Args:
        role_type:      Target career role (AI/ML, MLOps, DevOps, Data)
        skill_level:    User level (beginner / intermediate / advanced)
        top_skills:     List of (skill_name, score, freq) from SkillExtractor
        hours_per_week: Max learning hours available per week
        gap_skills:     [Phase 2] List of GapSkill objects from ResumeAnalyzer
        known_skills:   [Phase 2] Skills already on the resume (to skip)
    """

    def __init__(
        self,
        role_type: str = "AI/ML",
        skill_level: str = "intermediate",
        top_skills: Optional[List[Tuple[str, float, int]]] = None,
        hours_per_week: float = 10.0,
        gap_skills: Optional[List[Any]] = None,    # List[GapSkill]
        known_skills: Optional[List[str]] = None   # Already on resume
    ):
        self.role_type = role_type
        self.skill_level = skill_level
        self.top_skills = top_skills or []
        self.hours_per_week = hours_per_week
        self.gap_skills = gap_skills or []
        self.known_skills: set = {s.lower() for s in (known_skills or [])}
        self._plan: List[WeekPlan] = []
        self._gap_driven = len(self.gap_skills) > 0

    def _get_resource(self, skill: str) -> Tuple[str, str]:
        skill_lower = skill.lower()
        for key, resource in LEARNING_RESOURCES.items():
            if key in skill_lower or skill_lower in key:
                return resource["url"], resource["platform"]
        return LEARNING_RESOURCES["default"]["url"], LEARNING_RESOURCES["default"]["platform"]

    def _get_skill_category(self, skill: str) -> str:
        skill_lower = skill.lower()
        for category, data in SKILL_TAXONOMY.items():
            if skill_lower in [s.lower() for s in data["skills"]]:
                return category
        return "general"

    def _assign_priority(self, skill: str, week: int) -> str:
        category = self._get_skill_category(skill)
        if self.role_type in ROLE_FOCUS:
            primary = ROLE_FOCUS[self.role_type]["primary"]
            secondary = ROLE_FOCUS[self.role_type]["secondary"]
            if category in primary:
                return "HIGH"
            elif category in secondary:
                return "MEDIUM"
        return "LOW" if week > 2 else "MEDIUM"

    def _estimate_hours(self, score: float) -> float:
        cfg = SKILL_DIFFICULTY.get(self.skill_level, SKILL_DIFFICULTY["intermediate"])
        base = cfg["hours_per_skill"]
        multiplier = 1.3 if score > 2.0 else 1.0
        return round(min(base * multiplier, self.hours_per_week / 2), 1)

    def _make_task_from_gap(self, gap: Any, week: int) -> WeeklyTask:
        """Create a WeeklyTask from a GapSkill object."""
        url, platform = self._get_resource(gap.skill)
        hours = self._estimate_hours(gap.demand_score)
        return WeeklyTask(
            skill=gap.skill,
            category=gap.category,
            hours=hours,
            resource_url=url,
            platform=platform,
            priority=gap.demand_level,
            is_gap=True
        )

    def _make_task_from_market(self, skill: str, score: float, week: int) -> WeeklyTask:
        """Create a WeeklyTask from a market top-skill tuple."""
        url, platform = self._get_resource(skill)
        hours = self._estimate_hours(score)
        category = self._get_skill_category(skill)
        priority = self._assign_priority(skill, week)
        return WeeklyTask(
            skill=skill,
            category=category,
            hours=hours,
            resource_url=url,
            platform=platform,
            priority=priority,
            is_gap=False
        )

    def _add_practice_task(self, week: WeekPlan, remaining: float):
        """Fill leftover hours with a portfolio practice task."""
        if remaining >= 1.5:
            week.add_task(WeeklyTask(
                skill=f"Practice Project -- Week {week.week_number}",
                category="project",
                hours=round(remaining, 1),
                resource_url="https://github.com",
                platform="GitHub / Portfolio",
                priority="HIGH",
                is_gap=False
            ))

    def _fill_week(
        self,
        week: WeekPlan,
        skill_pool: list,
        max_skills: int,
        is_gap_pool: bool
    ) -> list:
        """
        Pull up to max_skills from skill_pool into week.
        Returns remaining pool items not used.
        """
        cfg = SKILL_DIFFICULTY.get(self.skill_level, SKILL_DIFFICULTY["intermediate"])
        remaining_hours = self.hours_per_week
        used = 0

        while skill_pool and used < max_skills and remaining_hours > 0:
            item = skill_pool.pop(0)

            # Skip known skills in gap mode
            skill_name = item.skill if is_gap_pool else item[0]
            if skill_name.lower() in self.known_skills and is_gap_pool:
                continue

            if is_gap_pool:
                task = self._make_task_from_gap(item, week.week_number)
            else:
                task = self._make_task_from_market(item[0], item[1], week.week_number)

            task.hours = min(task.hours, remaining_hours)
            week.add_task(task)
            remaining_hours -= task.hours
            used += 1

        return skill_pool

    def generate(self) -> "PlanGenerator":
        """Generate the 4-week learning plan. Returns self for chaining."""
        self._plan = []
        cfg = SKILL_DIFFICULTY.get(self.skill_level, SKILL_DIFFICULTY["intermediate"])
        max_per_week = cfg["max_skills_per_week"]
        today = datetime.now()

        themes = WEEK_THEMES if self._gap_driven else WEEK_THEMES_GENERIC

        if self._gap_driven:
            # Phase 2: Gap-driven plan
            # Partition gaps by priority
            high_gaps = [g for g in self.gap_skills if g.demand_level == "HIGH"]
            med_gaps  = [g for g in self.gap_skills if g.demand_level == "MEDIUM"]
            low_gaps  = [g for g in self.gap_skills if g.demand_level == "LOW"]

            # Market skills not already in gaps and not known
            gap_skill_names = {g.skill.lower() for g in self.gap_skills}
            market_extra = [
                (sk, sc, fr) for sk, sc, fr in self.top_skills
                if sk.lower() not in gap_skill_names and sk.lower() not in self.known_skills
            ]

            # Week assignments: W1=HIGH, W2=HIGH overflow+MEDIUM, W3=MEDIUM+LOW, W4=market extra
            week_pools = [
                (list(high_gaps), True),
                (list(med_gaps), True),
                (list(low_gaps) + [], True),
                (list(market_extra), False)
            ]
        else:
            # Phase 1 generic plan
            market_pool = [
                (sk, sc, fr) for sk, sc, fr in self.top_skills
                if sk.lower() not in self.known_skills
            ]
            chunk = max_per_week
            week_pools = [
                (list(market_pool[i * chunk:(i + 1) * chunk]), False)
                for i in range(4)
            ]

        for week_num in range(1, 5):
            theme = themes[week_num - 1]
            start = (today + timedelta(weeks=week_num - 1)).strftime("%Y-%m-%d")
            week = WeekPlan(week_number=week_num, theme=theme, start_date=start)

            pool, is_gap = week_pools[week_num - 1] if week_num <= len(week_pools) else ([], False)
            pool_copy = list(pool)

            used_hours = 0.0
            used_count = 0

            for item in pool_copy:
                if used_count >= max_per_week:
                    break
                skill_name = item.skill if is_gap else item[0]
                if skill_name.lower() in self.known_skills:
                    continue

                if is_gap:
                    task = self._make_task_from_gap(item, week_num)
                else:
                    task = self._make_task_from_market(item[0], item[1], week_num)

                available = self.hours_per_week - used_hours
                if available <= 0:
                    break
                task.hours = min(task.hours, available)
                week.add_task(task)
                used_hours += task.hours
                used_count += 1

            # Fill remaining hours with practice
            self._add_practice_task(week, self.hours_per_week - week.total_hours)
            self._plan.append(week)

        return self

    def get_plan(self) -> List[WeekPlan]:
        return self._plan

    def get_plan_dict(self) -> Dict:
        return {
            "generated_at": datetime.now().isoformat(),
            "role_type": self.role_type,
            "skill_level": self.skill_level,
            "hours_per_week": self.hours_per_week,
            "gap_driven": self._gap_driven,
            "total_weeks": len(self._plan),
            "total_hours": round(sum(w.total_hours for w in self._plan), 1),
            "weeks": [w.to_dict() for w in self._plan]
        }

    def print_plan(self):
        mode = "Gap-Driven" if self._gap_driven else "Market-Driven"
        print(f"\n{'='*62}")
        print(f"  CareerPilot AI -- 4-Week Learning Plan  [{mode}]")
        print(f"  Role: {self.role_type} | Level: {self.skill_level.title()}")
        print(f"{'='*62}")
        for week in self._plan:
            print(f"\n  WEEK {week.week_number}: {week.theme}")
            print(f"  Start: {week.start_date} | Total: {week.total_hours}h")
            print(f"  {'--'*28}")
            for task in week.tasks:
                gap_tag = " [GAP]" if task.is_gap else ""
                flag = ">>>" if task.priority == "HIGH" else (" >>" if task.priority == "MEDIUM" else "  >")
                print(f"  {flag} [{task.hours}h] {task.skill:<30} ({task.platform}){gap_tag}")
        total = sum(w.total_hours for w in self._plan)
        print(f"\n{'='*62}")
        print(f"  Total investment: {total:.1f}h over 4 weeks")
        print(f"{'='*62}\n")


# -- Quick test ----------------------------------------------------------------
if __name__ == "__main__":
    from pipelines.resume_analyzer import GapSkill

    gap_skills = [
        GapSkill("kubernetes", "devops_tools",  3.5, "HIGH",   10),
        GapSkill("mlflow",     "mlops_tools",   3.1, "HIGH",   9),
        GapSkill("terraform",  "devops_tools",  2.0, "MEDIUM", 6),
        GapSkill("airflow",    "data_engineering", 1.5, "MEDIUM", 5),
        GapSkill("dbt",        "data_engineering", 0.9, "LOW",    3),
    ]
    market = [
        ("python", 3.5, 15), ("pytorch", 3.1, 12), ("langchain", 2.9, 11),
    ]
    known = ["python", "docker", "fastapi"]

    gen = PlanGenerator(
        role_type="MLOps",
        skill_level="intermediate",
        top_skills=market,
        hours_per_week=10.0,
        gap_skills=gap_skills,
        known_skills=known
    )
    gen.generate()
    gen.print_plan()
