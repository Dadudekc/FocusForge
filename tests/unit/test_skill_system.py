import unittest
import json
import os
from pathlib import Path
from meta_skills import MetaSkill, MetaSkillManager
from skill_animations import DevlogWriter

class TestMetaSkill(unittest.TestCase):
    def setUp(self):
        self.skill = MetaSkill(
            name="TestSkill",
            xp=0,
            level=1,
            description="Test skill for unit testing",
            icon="🧪"
        )
        
    def test_initial_state(self):
        """Test initial skill state"""
        self.assertEqual(self.skill.name, "TestSkill")
        self.assertEqual(self.skill.xp, 0)
        self.assertEqual(self.skill.level, 1)
        self.assertEqual(self.skill.xp_to_next_level, 100)
        
    def test_xp_gain(self):
        """Test XP gain without level up"""
        self.skill.add_xp(50)
        self.assertEqual(self.skill.xp, 50)
        self.assertEqual(self.skill.level, 1)
        
    def test_level_up(self):
        """Test level up mechanics"""
        # Level up
        self.skill.add_xp(100)
        self.assertEqual(self.skill.level, 2)
        self.assertEqual(self.skill.xp, 0)  # XP resets after level up
        self.assertEqual(self.skill.xp_to_next_level, 200)  # Next level requires more XP
        
    def test_multiple_level_ups(self):
        """Test multiple level ups in one gain"""
        self.skill.add_xp(250)  # Should level up once, with 150 XP toward next level
        self.assertEqual(self.skill.level, 2)
        self.assertEqual(self.skill.xp, 150)  # 250 - 100
        self.assertEqual(self.skill.xp_to_next_level, 200)

class TestMetaSkillManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_skills.json"
        self.manager = MetaSkillManager(self.test_file)
        
    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("test_devlog.md"):
            os.remove("test_devlog.md")
            
    def test_initial_skills(self):
        """Test default skills are created"""
        skills = self.manager.get_all_skills()
        self.assertEqual(len(skills), 4)
        skill_names = {skill.name for skill in skills}
        self.assertEqual(skill_names, {"Grit", "Discipline", "Charisma", "Precision"})
        
    def test_skill_persistence(self):
        """Test skills are saved and loaded correctly"""
        # Add XP to a skill
        self.manager.add_xp("Grit", 50)
        
        # Create new manager instance (should load saved data)
        new_manager = MetaSkillManager(self.test_file)
        grit = new_manager.get_skill("Grit")
        self.assertEqual(grit.xp, 50)
        
    def test_xp_gain(self):
        """Test XP gain through manager"""
        message = self.manager.add_xp("Grit", 50)
        self.assertEqual(message, "[+50 Grit]")
        grit = self.manager.get_skill("Grit")
        self.assertEqual(grit.xp, 50)
        
    def test_level_up(self):
        """Test level up through manager"""
        message = self.manager.add_xp("Grit", 100)
        self.assertEqual(message, "🎉 Grit leveled up to 2!")
        grit = self.manager.get_skill("Grit")
        self.assertEqual(grit.level, 2)
        
    def test_invalid_skill(self):
        """Test handling of invalid skill names"""
        message = self.manager.add_xp("InvalidSkill", 50)
        self.assertIsNone(message)
        
    def test_skill_progress(self):
        """Test skill progress tracking"""
        self.manager.add_xp("Grit", 75)
        current_xp, next_level = self.manager.get_skill_progress("Grit")
        self.assertEqual(current_xp, 75)
        self.assertEqual(next_level, 100)

class TestDevlogWriter(unittest.TestCase):
    def setUp(self):
        self.devlog = DevlogWriter("test_devlog.md")
        
    def tearDown(self):
        if os.path.exists("test_devlog.md"):
            os.remove("test_devlog.md")
            
    def test_xp_log(self):
        """Test XP gain logging"""
        self.devlog.log_xp_event("Grit", 50, "Test Task")
        
        with open("test_devlog.md", "r") as f:
            content = f.read()
            self.assertIn("[+50 Grit]", content)
            self.assertIn("Test Task", content)
            
    def test_level_up_log(self):
        """Test level up logging"""
        self.devlog.log_xp_event("Grit", 100, "Test Task", True)
        with open("test_devlog.md", "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Grit Level Up!", content)
            self.assertIn("has reached a new level of mastery", content)

def run_simulation():
    """Run a simulation of the skill system"""
    print("\n🧪 Running Skill System Simulation")
    print("=" * 40)
    
    # Initialize manager
    manager = MetaSkillManager("simulation_skills.json")
    devlog = DevlogWriter("simulation_devlog.md")
    
    # Simulate task completion
    tasks = [
        ("Complete project proposal", "Grit", 25),
        ("Code review", "Precision", 15),
        ("Team meeting", "Charisma", 10),
        ("Debug complex issue", "Grit", 30),
        ("Document API", "Discipline", 20)
    ]
    
    for task_name, skill, xp in tasks:
        print(f"\n📝 Task: {task_name}")
        print(f"🎯 Target: {skill}")
        print(f"✨ XP: {xp}")
        
        message = manager.add_xp(skill, xp)
        if message:
            print(f"💫 Result: {message}")
            
            # Log to devlog
            leveled_up = "leveled up" in message
            devlog.log_xp_event(skill, xp, task_name, leveled_up)
            
            # Show current progress
            skill_obj = manager.get_skill(skill)
            print(f"📊 Progress: {skill_obj.xp}/{skill_obj.xp_to_next_level} XP")
            print(f"📈 Level: {skill_obj.level}")
    
    print("\n" + "=" * 40)
    print("✅ Simulation Complete")
    print("📊 Final Stats:")
    
    for skill in manager.get_all_skills():
        print(f"\n{skill.icon} {skill.name}")
        print(f"  Level: {skill.level}")
        print(f"  XP: {skill.xp}/{skill.xp_to_next_level}")

if __name__ == "__main__":
    # Run unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # Run simulation
    run_simulation() 