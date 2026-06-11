import re

class TranscriptCleaner:
    @staticmethod
    def clean(transcript: str) -> str:
        """
        Cleans the transcript by normalizing spaces, removing empty lines,
        and preserving speaker labels and timestamps.
        """
        lines = transcript.split('\n')
        cleaned_lines = []
        for line in lines:
            # 1. Remove excessive spaces
            line = re.sub(r'[ \t]+', ' ', line)
            line = line.strip()
            
            # 2. Remove empty lines
            if not line:
                continue
            
            cleaned_lines.append(line)
            
        # Join lines back with a single newline to preserve boundaries
        return "\n".join(cleaned_lines)
