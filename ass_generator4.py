import json
from datetime import timedelta

def format_timestamp(seconds):
    """Converts seconds to ASS time format (h:mm:ss.cs)"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    centiseconds = int((td.microseconds / 10000))
    return f"{hours}:{minutes:02}:{seconds:02}.{centiseconds:02}"

def main():
    # Load the JSON data from the file
    with open('Jimmy Kimmel Asks Keanu Reeves Random Questions.json', 'r') as file:
        data = json.load(file)

    # ASS header
    ass_lines = [
        "[Script Info]",
        "Title: Subtitle",
        "ScriptType: v4.00+", 
        "Collisions: Normal", 
        "PlayDepth: 0",
        "", 
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1",
        "", 
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    # Build the events
    for segment in data['segments']:
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        full_text = segment['text']  # Do not escape commas

        # Create an event for the whole sentence with white color
        sentence_line = f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{full_text}"
        ass_lines.append(sentence_line)

        # Create a highlight event for each word with yellow highlight
        for word in segment['words']:
            word_start = format_timestamp(word['start'])
            word_end = format_timestamp(word['end'])
            word_text = word['word']
            # Use string concatenation for the highlight
            highlighted_text = full_text.replace(
                word_text, "{\\c&H00FFFF00&}" + word_text + "{\\c&H00FFFFFF&}"
            )
            highlight_line = f"Dialogue: 1,{word_start},{word_end},Default,,0,0,0,,{highlighted_text}"
            ass_lines.append(highlight_line)
    
    # Write to .ass file
    with open('output.ass', 'w') as outfile:
        for line in ass_lines:
            outfile.write(line + "\n")

if __name__ == "__main__":
    main()