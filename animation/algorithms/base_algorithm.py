from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class Message:
    from_processor: int
    to_processor: int
    data: Any
    step: int
    message_type: str = "data"
    progress: float = 0.0
    
    def __repr__(self):
        return f"Msg({self.from_processor}→{self.to_processor})"

@dataclass
class AlgorithmStep:
    step_number: int
    messages: List[Message] = field(default_factory=list)
    description: str = ""
    
    def __repr__(self):
        return f"Step {self.step_number}: {len(self.messages)} msgs"


class BaseAlgorithm(ABC):
    def __init__(self, name: str):
        self.name = name
        self.steps: List[AlgorithmStep] = []
        
    @abstractmethod
    def generate_steps(self, topology, params) -> List[AlgorithmStep]:
        pass
    
    def get_step(self, step_number: int) -> AlgorithmStep:
        if 0 <= step_number < len(self.steps):
            return self.steps[step_number]
        return None
    
    def total_steps(self) -> int:
        return len(self.steps)