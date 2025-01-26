import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from src.utils.helper import ComplexityAnalyser

class BribeManager:
    def __init__(self):
        self.baseBribe = 500
        self.startYear = 2025
        self.collectedBribe = 0
        self.requiredBribe = 0
        self.parichay = None
        self.profiles = {
            "JANTA": 1.0,
            "STUDENT": 0.5,
            "CHACHA VIDHAYAK HAI": 0.0,
            "BABU SAHEB": 1.0,
            "NETA JI": 0.0,
        }

    def calculate_base_bribe(self):
        currentYear = datetime.datetime.now().year
        yearsSinceBase = currentYear - self.startYear
        return self.baseBribe * (1.5 ** yearsSinceBase)

    def set_parichay(self, profile):
        self.parichay = profile.upper()
        if (self.parichay not in self.profiles):
            raise ValueError(f"Unknown parichay: {profile}")
        return self.profiles[self.parichay]

    def calculate_bribe_required(self, ast):
        analyzer = ComplexityAnalyser()
        timeComplexityFactor = analyzer.calculate_time_complexity(ast)
        baseBribe = self.calculate_base_bribe()
        self.requiredBribe = baseBribe * timeComplexityFactor
                
        return self.requiredBribe

    def collect_bribe(self, bribeAmount):
        self.collectedBribe += bribeAmount
        print(f"Bribe collected so far: {self.collectedBribe}")

    def validate_bribe(self):
        reductionFactor = self.profiles[self.parichay]
        self.requiredBribe *= reductionFactor
        if (self.parichay == "CHACHA VIDHAYAK HAI"):
            print("Sir aapka kaam already ho chuka hai. Koi chinta nahi, aap toh apne hai!")
        elif (self.parichay == "NETA JI"):
            print("Neta Ji, Chinta mat kijiye, case register ho gaya hai. Aapse kya ghoos lena")

        if (self.collectedBribe < self.requiredBribe):
            raise RuntimeError(f"Your work progress has been halted due to insufficient sweet packets.")

        if (self.parichay == "JANTA"):
            print("Aam aadmi ki ghoos seedhi seedhi hai. Bas files clear hone ka wait kijiye!")
        elif (self.parichay == "STUDENT"):
            print("Discount laga diya hai! Ghoos student-friendly bana di gayi hai!")
        elif (self.parichay == "BABU SAHEB"):
            print("Aapka kaam bhi hoga, aur aapko {self.collectedBribe} bhi wapis mil gaye hai. Babu ji ka style hi alag hai!")

    def reset(self):
        self.requiredBribe = 0
        self.collectedBribe = 0