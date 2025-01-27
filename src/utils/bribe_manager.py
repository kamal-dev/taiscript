import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from src.utils.helper import ComplexityAnalyser
from collections import deque

class BribeManager:
    def __init__(self):
        self.baseBribe = 500
        self.startYear = 2025
        self.bribeQueue = deque()
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
        self.currentTimeComplexity = "LINEAR"
        self.loopDepth = 0
        self.loopDeducted = set()

    def calculate_base_bribe(self):
        """
        Calculates the base bribe based on the current year.

        The base bribe increases 1.5 times for each year since startign year.

        Returns:
            float: Returns the new base bribe value.
        """
        currentYear = datetime.datetime.now().year
        yearsSinceBase = currentYear - self.startYear
        return self.baseBribe * (1.5 ** yearsSinceBase)

    def set_parichay(self, profile):
        """
        Sets the parichay for the bribe system.

        Args:
            profile (str): The parichay - "Janta", "Babu Saheb", etc

        Raises:
            ValueError: Returns an error if the profile is not recognized

        Returns:
            float: Returns the reduction factor for the profile.
        """
        self.parichay = profile.upper()
        if (self.parichay not in self.profiles):
            raise ValueError(f"Unknown parichay: {profile}")
        return self.profiles[self.parichay]

    def collect_bribe(self, bribeAmount):
        """
        Collects the bribe and adds it to the queue

        Args:
            bribeAmount (float): The amount to be added as the bribe
        """
        self.bribeQueue.append(bribeAmount)

    def update_required_bribe(self):
        """
        Updates the bribe amount based on parichay of the profile.
        """
        reductionFactor = self.profiles[self.parichay]
        self.baseBribe *= reductionFactor

    def validate_bribe(self, statement):
        """
        Validates the bribe based on the type of statement

        Args:
            statement (dict): Dictionary containing the statement details

        Raises:
            RuntimeError: If the collected bribe is insufficient for the code to execute (based on time complexity)
        """
        # TODO: Add better logs of exception for different Parichay Type
        if (statement["type"] == "LOOP"):
            if (self.loopDepth == 0 and self.currentTimeComplexity == "LINEAR"):
                self.reset()
                self.currentTimeComplexity = "NESTED"

                while (self.bribeQueue):
                    self.collectedBribe += self.bribeQueue.pop()

            if (self.loopDepth not in self.loopDeducted):
                self.collectedBribe -= self.baseBribe
                self.loopDeducted.add(self.loopDepth)

            if self.collectedBribe < 0:
                raise RuntimeError(f"Itne me kya hoga! Thoda aur adjust karo, tabhi '{statement["type"]}' ki file aage badhegi.\nPass {abs(self.collectedBribe)} more under the table.")
        else:

            if (self.loopDepth > 0):
                return

            if (self.currentTimeComplexity == "NESTED"):
                self.reset()
                self.currentTimeComplexity = "LINEAR"

            while(self.bribeQueue):
                self.collectedBribe += self.bribeQueue.pop()

            if (self.collectedBribe < self.baseBribe):
                shortfall = self.baseBribe - self.collectedBribe
                raise RuntimeError(f"Itne me kya hoga! Thoda aur adjust karo, tabhi '{statement["type"]}' ki file aage badhegi.\nPass {shortfall} more under the table.")

    def reset(self):
        """
        Resets the bribe manager state
        """
        self.requiredBribe = 0
        self.collectedBribe = 0
        self.loopDeducted.clear()

    def loop_inc(self):
        """
        Increment the loop depth counter
        """
        self.loopDepth += 1

    def loop_dec(self):
        """
        Decrement the loop depth counter and remove loop deduction if current depth has been processed.
        """
        if self.loopDepth in self.loopDeducted:
            self.loopDeducted.remove(self.loopDepth)
        self.loopDepth -= 1