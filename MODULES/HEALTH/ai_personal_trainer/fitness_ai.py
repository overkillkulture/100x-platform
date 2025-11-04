#!/usr/bin/env python3
"""
💪 AI PERSONAL TRAINER

24/7 AI Fitness Coach with Claude AI + Computer Vision Form Correction

Author: Consciousness Revolution
License: MIT
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


@dataclass
class UserProfile:
    """User fitness profile"""
    user_id: str
    name: str
    age: int
    weight: float  # lbs
    height: int  # inches
    fitness_level: str  # beginner, intermediate, advanced
    goal: str  # lose_weight, build_muscle, endurance, general_fitness
    equipment: List[str]
    schedule: str  # e.g., "4 days/week"
    injuries: List[str] = None
    dietary_restrictions: List[str] = None
    created_at: str = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.injuries is None:
            self.injuries = []
        if self.dietary_restrictions is None:
            self.dietary_restrictions = []


@dataclass
class Exercise:
    """Individual exercise"""
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None  # lbs, None for bodyweight
    rest_seconds: int = 60
    instructions: str = ""
    video_url: Optional[str] = None
    muscle_groups: List[str] = None

    def __post_init__(self):
        if self.muscle_groups is None:
            self.muscle_groups = []


@dataclass
class Workout:
    """Complete workout session"""
    workout_id: str
    name: str
    day_of_week: str
    exercises: List[Exercise]
    warmup: List[str]
    cooldown: List[str]
    estimated_duration: int  # minutes
    difficulty: str  # easy, medium, hard


@dataclass
class WorkoutProgram:
    """Complete training program"""
    program_id: str
    name: str
    description: str
    weeks: int
    workouts: List[Workout]
    goal: str
    created_at: str = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class FormAnalysis:
    """Computer vision form analysis results"""
    exercise: str
    form_quality: int  # 0-100 score
    rep_count: int
    corrections: List[str]
    good_points: List[str]
    injury_risk: str  # low, medium, high
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class Meal:
    """Meal nutrition information"""
    meal_name: str
    foods: List[str]
    calories: int
    protein: float  # grams
    carbs: float
    fat: float
    fiber: float = 0.0
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class DailyNutrition:
    """Daily nutrition targets and progress"""
    date: str
    calorie_target: int
    protein_target: float
    carbs_target: float
    fat_target: float
    calories_consumed: int = 0
    protein_consumed: float = 0.0
    carbs_consumed: float = 0.0
    fat_consumed: float = 0.0
    meals: List[Meal] = None

    def __post_init__(self):
        if self.meals is None:
            self.meals = []


class WorkoutPlanner:
    """AI-powered workout program generation"""

    def __init__(self, anthropic_api_key: str = None):
        self.api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required")
        self.claude = Anthropic(api_key=self.api_key)

    def generate_program(self, profile: UserProfile) -> WorkoutProgram:
        """AI generates personalized 12-week workout program"""

        prompt = f"""Create personalized 12-week workout program:

USER PROFILE:
- Age: {profile.age}
- Weight: {profile.weight} lbs
- Height: {profile.height} inches
- Fitness level: {profile.fitness_level}
- Goal: {profile.goal}
- Equipment: {', '.join(profile.equipment)}
- Schedule: {profile.schedule}
- Injuries: {', '.join(profile.injuries) if profile.injuries else "None"}

REQUIREMENTS:
1. Progressive overload (gradually increase difficulty)
2. Balanced muscle development
3. Appropriate for fitness level
4. Achieves stated goal
5. Fits schedule
6. Works around injuries

Create program with:
- Program name
- Weekly workout split
- 4-6 exercises per workout
- Sets, reps, rest periods
- Warmup and cooldown
- Progression plan

Respond in JSON format:
{{
  "program_name": "Intermediate Muscle Building",
  "description": "4-day split focused on hypertrophy",
  "weeks": 12,
  "workouts": [
    {{
      "name": "Chest & Triceps",
      "day": "Monday",
      "exercises": [
        {{
          "name": "Barbell Bench Press",
          "sets": 4,
          "reps": 8,
          "weight": 155,
          "rest_seconds": 90,
          "instructions": "Lower to chest, press up explosively",
          "muscle_groups": ["chest", "triceps", "shoulders"]
        }}
      ],
      "warmup": ["5 min cardio", "Dynamic stretches", "Light bench press sets"],
      "cooldown": ["Chest stretches", "Tricep stretches"],
      "estimated_duration": 60,
      "difficulty": "medium"
    }}
  ]
}}
"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        result_text = response.content[0].text
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}') + 1
        program_data = json.loads(result_text[start_idx:end_idx])

        # Convert to WorkoutProgram object
        workouts = []
        for w in program_data['workouts']:
            exercises = [Exercise(**e) for e in w['exercises']]
            workout = Workout(
                workout_id=f"workout_{len(workouts) + 1}",
                name=w['name'],
                day_of_week=w['day'],
                exercises=exercises,
                warmup=w['warmup'],
                cooldown=w['cooldown'],
                estimated_duration=w['estimated_duration'],
                difficulty=w['difficulty']
            )
            workouts.append(workout)

        program = WorkoutProgram(
            program_id=f"program_{int(time.time())}",
            name=program_data['program_name'],
            description=program_data['description'],
            weeks=program_data['weeks'],
            workouts=workouts,
            goal=profile.goal
        )

        return program

    def adapt_workout(self, workout: Workout, performance_feedback: Dict) -> Workout:
        """AI adapts workout based on user performance"""

        prompt = f"""Adapt workout based on user performance:

CURRENT WORKOUT: {workout.name}
EXERCISES:
{json.dumps([asdict(e) for e in workout.exercises], indent=2)}

USER FEEDBACK:
{json.dumps(performance_feedback, indent=2)}

Adjust:
1. Increase weight if user found it too easy
2. Decrease weight if user struggled with form
3. Add or remove exercises based on time available
4. Modify exercises if user reported pain

Return updated exercises in same JSON format.
"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse and update workout
        result_text = response.content[0].text
        start_idx = result_text.find('[')
        end_idx = result_text.rfind(']') + 1
        updated_exercises = json.loads(result_text[start_idx:end_idx])

        workout.exercises = [Exercise(**e) for e in updated_exercises]
        return workout


class FormChecker:
    """Computer vision-based form analysis (simulated - would use MediaPipe in production)"""

    def __init__(self):
        # In production, this would initialize MediaPipe Pose Detection
        self.model_loaded = True

    def analyze_form(self, exercise: str, video_frame: Optional[bytes] = None) -> FormAnalysis:
        """
        Analyze exercise form from video frame

        In production, this would:
        1. Use MediaPipe to detect 33 body landmarks
        2. Calculate joint angles
        3. Compare to ideal form for the exercise
        4. Provide real-time corrections

        For demo, we'll simulate the analysis
        """

        # Simulated analysis (in production, would process video frame)
        form_quality = 85  # 0-100 score
        rep_count = 8
        corrections = []
        good_points = []
        injury_risk = "low"

        # Example corrections based on exercise type
        if exercise.lower() == "squat":
            good_points.append("Back is straight")
            good_points.append("Depth is good (below parallel)")
            corrections.append("Push knees out slightly to match toe angle")
            form_quality = 82

        elif exercise.lower() == "bench press":
            good_points.append("Elbows at proper 45° angle")
            corrections.append("Arch your back slightly more for stability")
            form_quality = 88

        elif exercise.lower() == "deadlift":
            good_points.append("Neutral spine maintained")
            corrections.append("Keep bar closer to shins during ascent")
            injury_risk = "medium"  # Deadlift is higher risk if form breaks down
            form_quality = 78

        analysis = FormAnalysis(
            exercise=exercise,
            form_quality=form_quality,
            rep_count=rep_count,
            corrections=corrections,
            good_points=good_points,
            injury_risk=injury_risk
        )

        return analysis

    def count_reps(self, exercise: str, video_stream: Optional[bytes] = None) -> int:
        """
        Count reps automatically using computer vision

        In production, this would:
        1. Track joint angles over time
        2. Detect complete range of motion
        3. Only count reps with good form
        """
        # Simulated rep counting
        return 10


class NutritionCoach:
    """AI-powered nutrition planning and tracking"""

    def __init__(self, anthropic_api_key: str = None):
        self.api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required")
        self.claude = Anthropic(api_key=self.api_key)

    def generate_meal_plan(self, profile: UserProfile, calorie_target: int,
                          macro_ratios: Dict[str, float]) -> Dict:
        """AI generates 7-day meal plan"""

        prompt = f"""Create 7-day meal plan:

USER:
- Age: {profile.age}
- Weight: {profile.weight} lbs
- Goal: {profile.goal}
- Dietary restrictions: {', '.join(profile.dietary_restrictions) if profile.dietary_restrictions else "None"}

TARGETS:
- Calories: {calorie_target}/day
- Protein: {macro_ratios['protein']}g/day
- Carbs: {macro_ratios['carbs']}g/day
- Fat: {macro_ratios['fat']}g/day

Create balanced meal plan with:
- Breakfast, lunch, dinner, 2 snacks per day
- Variety (different meals each day)
- Simple recipes (15-30 min prep)
- Grocery list

Respond in JSON format with 7 days of meals.
"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.content[0].text
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}') + 1
        meal_plan = json.loads(result_text[start_idx:end_idx])

        return meal_plan

    def analyze_meal_photo(self, photo_path: str) -> Meal:
        """
        Analyze meal from photo and estimate nutrition

        In production, this would:
        1. Use computer vision to identify foods
        2. Estimate portion sizes
        3. Look up nutrition data
        4. Calculate totals

        For demo, we'll simulate
        """

        # Simulated food recognition
        foods = ["Grilled chicken breast (6 oz)", "Brown rice (1 cup)", "Steamed broccoli (1.5 cups)"]

        # Simulated nutrition calculation
        meal = Meal(
            meal_name="Lunch",
            foods=foods,
            calories=485,
            protein=52.0,
            carbs=54.0,
            fat=8.0,
            fiber=7.0
        )

        return meal

    def get_meal_recommendations(self, remaining_macros: Dict) -> List[str]:
        """AI suggests meals based on remaining daily macros"""

        prompt = f"""Suggest meals based on remaining macros:

REMAINING TODAY:
- Calories: {remaining_macros['calories']}
- Protein: {remaining_macros['protein']}g
- Carbs: {remaining_macros['carbs']}g
- Fat: {remaining_macros['fat']}g

Suggest 3 meals that fit these targets.
Keep suggestions simple and quick to prepare.
"""

        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        suggestions = response.content[0].text.split('\n')
        # Filter out empty lines
        suggestions = [s.strip() for s in suggestions if s.strip()]

        return suggestions[:3]


class PersonalTrainer:
    """Main AI Personal Trainer class"""

    def __init__(self, anthropic_api_key: str = None):
        self.api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.workout_planner = WorkoutPlanner(self.api_key)
        self.form_checker = FormChecker()
        self.nutrition_coach = NutritionCoach(self.api_key)
        self.user_profiles: Dict[str, UserProfile] = {}
        self.programs: Dict[str, WorkoutProgram] = {}

    def create_profile(self, **kwargs) -> UserProfile:
        """Create user fitness profile"""
        profile = UserProfile(
            user_id=f"user_{int(time.time())}",
            **kwargs
        )
        self.user_profiles[profile.user_id] = profile
        print(f"✅ Profile created for {profile.name}")
        return profile

    def generate_program(self, profile: UserProfile) -> WorkoutProgram:
        """Generate personalized workout program"""
        print(f"\n🧠 AI generating personalized program for {profile.name}...")
        program = self.workout_planner.generate_program(profile)
        self.programs[program.program_id] = program
        print(f"✅ Program created: {program.name}")
        print(f"   Duration: {program.weeks} weeks")
        print(f"   Workouts: {len(program.workouts)}")
        return program

    def start_workout(self, workout: Workout):
        """Guide user through workout with voice coaching"""
        print(f"\n🏋️ Starting Workout: {workout.name}")
        print(f"   Estimated duration: {workout.estimated_duration} minutes")
        print(f"   Difficulty: {workout.difficulty}")

        # Warmup
        print(f"\n🔥 WARMUP:")
        for item in workout.warmup:
            print(f"   - {item}")
        time.sleep(1)

        # Exercises
        for i, exercise in enumerate(workout.exercises, 1):
            print(f"\n💪 Exercise {i}/{len(workout.exercises)}: {exercise.name}")
            print(f"   Target: {exercise.sets} sets × {exercise.reps} reps")
            if exercise.weight:
                print(f"   Weight: {exercise.weight} lbs")
            print(f"   Instructions: {exercise.instructions}")

            # Simulate form checking
            print(f"   📹 Analyzing your form...")
            time.sleep(0.5)

            form_analysis = self.form_checker.analyze_form(exercise.name)

            print(f"   Form Quality: {form_analysis.form_quality}/100")

            if form_analysis.good_points:
                print(f"   ✅ Good: {', '.join(form_analysis.good_points)}")

            if form_analysis.corrections:
                print(f"   ⚠️  Corrections: {', '.join(form_analysis.corrections)}")

            print(f"   🎯 Rest {exercise.rest_seconds} seconds...")
            time.sleep(1)

        # Cooldown
        print(f"\n🧘 COOLDOWN:")
        for item in workout.cooldown:
            print(f"   - {item}")

        print(f"\n✅ Workout Complete! Great job!")

    def track_nutrition(self, meal_photo: Optional[str] = None) -> DailyNutrition:
        """Track nutrition for the day"""

        print(f"\n🍽️  NUTRITION TRACKING")

        # Analyze meal
        if meal_photo:
            meal = self.nutrition_coach.analyze_meal_photo(meal_photo)
            print(f"   Meal detected: {', '.join(meal.foods)}")
            print(f"   Calories: {meal.calories}")
            print(f"   Protein: {meal.protein}g")
            print(f"   Carbs: {meal.carbs}g")
            print(f"   Fat: {meal.fat}g")

        # Get daily progress
        daily_nutrition = DailyNutrition(
            date=datetime.now().date().isoformat(),
            calorie_target=2200,
            protein_target=180,
            carbs_target=220,
            fat_target=60
        )

        # Add meal
        if meal_photo:
            daily_nutrition.meals.append(meal)
            daily_nutrition.calories_consumed += meal.calories
            daily_nutrition.protein_consumed += meal.protein
            daily_nutrition.carbs_consumed += meal.carbs
            daily_nutrition.fat_consumed += meal.fat

        # Calculate remaining
        cal_remaining = daily_nutrition.calorie_target - daily_nutrition.calories_consumed
        protein_remaining = daily_nutrition.protein_target - daily_nutrition.protein_consumed

        print(f"\n📊 Daily Progress:")
        print(f"   Calories: {daily_nutrition.calories_consumed} / {daily_nutrition.calorie_target} ({cal_remaining} remaining)")
        print(f"   Protein: {daily_nutrition.protein_consumed}g / {daily_nutrition.protein_target}g ({protein_remaining}g remaining)")

        # AI recommendations
        if cal_remaining > 300 and protein_remaining > 20:
            print(f"\n💡 AI Recommendations:")
            suggestions = self.nutrition_coach.get_meal_recommendations({
                'calories': cal_remaining,
                'protein': protein_remaining,
                'carbs': daily_nutrition.carbs_target - daily_nutrition.carbs_consumed,
                'fat': daily_nutrition.fat_target - daily_nutrition.fat_consumed
            })
            for suggestion in suggestions:
                print(f"   - {suggestion}")

        return daily_nutrition


def demo():
    """Demo the AI Personal Trainer system"""

    print("=" * 70)
    print("💪 AI PERSONAL TRAINER - DEMO")
    print("=" * 70)

    # Initialize trainer
    trainer = PersonalTrainer()

    # Create user profile
    print("\n👤 CREATING USER PROFILE...")
    profile = trainer.create_profile(
        name="John",
        age=32,
        weight=180,
        height=72,
        fitness_level="intermediate",
        goal="build_muscle",
        equipment=["dumbbells", "barbell", "bench", "squat rack"],
        schedule="4 days/week",
        injuries=[]
    )

    # Generate workout program
    program = trainer.generate_program(profile)

    # Show program details
    print(f"\n📋 WORKOUT PROGRAM: {program.name}")
    print(f"   Description: {program.description}")
    print(f"   Duration: {program.weeks} weeks")
    print(f"\n   Workout Split:")
    for workout in program.workouts:
        print(f"   - {workout.day_of_week}: {workout.name}")

    # Start today's workout (first workout)
    print(f"\n" + "=" * 70)
    today_workout = program.workouts[0]
    trainer.start_workout(today_workout)

    # Track nutrition
    print(f"\n" + "=" * 70)
    trainer.track_nutrition(meal_photo="lunch.jpg")

    print(f"\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)


def cli():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AI Personal Trainer - 24/7 Fitness Coach"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo of AI personal trainer"
    )
    parser.add_argument(
        "--generate-program",
        action="store_true",
        help="Generate workout program"
    )

    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.generate_program:
        trainer = PersonalTrainer()
        # Interactive program generation would go here
        print("Interactive program generation not yet implemented.")
        print("Use --demo to see example.")
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
