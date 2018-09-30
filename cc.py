# blood detected
# limb removal detected


class BodyPartInjuryDetector:
    def __init__(self, body_part):
        self.is_bleeding = False
        self.is_removed = False
        self.body_part = body_part

    def update_values(self, is_bleeding, is_removed):
        self.is_bleeding = is_bleeding
        self.is_removed = is_removed

    def get_json_values(self):
        if not self.is_bleeding and not self.is_removed:
            return {}
        return {
            'no': self.body_part,
            'inj': 1 if self.is_bleeding else 2,
            'something': 2
        }
