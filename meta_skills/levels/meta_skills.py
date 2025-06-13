import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from core.utils.database import Database

@dataclass
class MetaSkill:
    name: str
    xp: int
    level: int
    description: str
    icon: str
    
    def __init__(self, name, xp=0, level=1, description="", icon="⭐"):
        self.name = name
        self.xp = xp
        self.level = level
        self.description = description
        self.icon = icon
        self.xp_to_next_level = self._calculate_xp_for_level(level)
        
    def _calculate_xp_for_level(self, level):
        """Calculate XP required for next level"""
        return 100 * level
        
    def add_xp(self, amount):
        """Add XP to the skill, handling level ups"""
        self.xp += amount
        levels_gained = 0
        
        # Handle multiple level ups if XP exceeds next level
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = self._calculate_xp_for_level(self.level)
            levels_gained += 1
            
        return levels_gained > 0
        
    def to_dict(self):
        """Convert skill to dictionary for saving"""
        return {
            "name": self.name,
            "xp": self.xp,
            "level": self.level,
            "description": self.description,
            "icon": self.icon
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create skill from dictionary"""
        return cls(
            name=data["name"],
            xp=data["xp"],
            level=data["level"],
            description=data["description"],
            icon=data["icon"]
        )

class MetaSkillManager:
    def __init__(self, skills_file: str = "meta_skills.json"):
        self.skills_file = skills_file
        self.skills: Dict[str, MetaSkill] = {}
        self.load_skills()
        
    def load_skills(self):
        try:
            with open(self.skills_file, "r") as f:
                data = json.load(f)
                for skill_data in data["skills"]:
                    skill = MetaSkill(**skill_data)
                    self.skills[skill.name] = skill
        except FileNotFoundError:
            # Initialize default skills
            self.skills = {
                "Grit": MetaSkill("Grit", 0, 1, "Perseverance through challenges", "🧠"),
                "Discipline": MetaSkill("Discipline", 0, 1, "Consistent task completion", "⚡"),
                "Charisma": MetaSkill("Charisma", 0, 1, "Social and communication skills", "✨"),
                "Precision": MetaSkill("Precision", 0, 1, "Attention to detail and accuracy", "🎯")
            }
            self.save_skills()
            
    def save_skills(self):
        data = {
            "skills": [asdict(skill) for skill in self.skills.values()]
        }
        with open(self.skills_file, "w") as f:
            json.dump(data, f, indent=2)
            
    def add_xp(self, skill_name: str, amount: int) -> Optional[str]:
        """Add XP to a skill and return level up message if applicable"""
        if skill_name in self.skills:
            skill = self.skills[skill_name]
            old_level = skill.level
            leveled_up = skill.add_xp(amount)
            self.save_skills()
            
            if leveled_up:
                return f"🎉 {skill_name} leveled up to {skill.level}!"
            return f"[+{amount} {skill_name}]"
        return None
    
    def get_skill(self, name: str) -> Optional[MetaSkill]:
        return self.skills.get(name)
    
    def get_all_skills(self) -> List[MetaSkill]:
        return list(self.skills.values())
    
    def get_skill_progress(self, name: str) -> tuple[int, int]:
        """Return (current_xp, xp_to_next_level)"""
        skill = self.get_skill(name)
        if skill:
            return skill.xp, skill.xp_to_next_level
        return 0, 0

class MetaSkills:
    def __init__(self):
        self.db = Database()
        self.skills = self.load_skills()
        self.xp = 0
        self.level = 1

    # ... rest of the file remains unchanged ... 