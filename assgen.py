
ass_header = '''
[Script Info]
Title: My Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Sans,16,&H00FFFFFF,&H000019FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0.8,0,2,50,50,24,1
Style: Small,Sans,10,&H00FFFFFF,&H000019FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0.8,0,8,50,50,258,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''

def format_srt_time(seconds):
    ms= seconds % 1
    s = int(seconds % 60)
    minutes = seconds / 60
    m = int(minutes % 60)
    hours = minutes / 60
    h = int(hours % 60)

    return '%02d:%02d:%02d,%03d' % (h,m,s,ms*1000)


def format_ass_time(seconds):
    ms= seconds % 1
    s = int(seconds % 60)
    minutes = seconds / 60
    m = int(minutes % 60)
    hours = minutes / 60
    h = int(hours % 60)

    return '%01d:%02d:%02d.%02d' % (h,m,s,ms*100)

# This function generates an ASS subtitle file for a list of segments.
# It takes the segments, the output file name, and an optional boolean argument to indicate if the subtitle 
# should be appended to an existing file instead of overwriting it.
def gen_subtitles(segments, outname, append=False):
    # Open the output file for writing or appending
    t = open(outname, 'a' if append else 'w', encoding='utf-8')

    # Write the ASS subtitle file header
    if not append:
        t.write(ass_header)

    # Set the style based on whether the subtitle is being appended or not
    style = 'Small' if append else 'Default'

    try:
        # Iterate through each segment and generate the corresponding subtitle lines
        for i, segment in enumerate(segments):
            # Format the start and end times for the subtitle line
            start_time = format_srt_time(segment.start)
            end_time = format_srt_time(segment.end)

            # Replace any newline characters in the segment text with a space
            text = segment.text.replace('\n', ' ')

            # Create the subtitle line with the index, start and end times, and segment text
            line = f"{i+1}\n{start_time} --> {end_time}\n{text}"

            # Print the segment information to the console
            print("[%s -> %s] %s" % (start_time, end_time, segment.text))

            # Write the subtitle line to the output file
            # f.write(line+'\n\n')

            # if word_ts:
            # Iterate through each word in the segment and generate the corresponding subtitle lines
            pos = 0
            last_end = segment.start
            if segment.words is not None:
                for word in segment.words:
                    st = word.start
                    ed = word.end
                    start_time = format_ass_time(st)
                    end_time = format_ass_time(ed)

                    # If the current word starts after the end of the last word, generate a subtitle line for the gap
                    if st > last_end:
                        line = f"Dialogue: 0,{format_ass_time(last_end)},{format_ass_time(st)},{style},,0,0,0,,{segment.text}"
                        t.write(line+'\n')

                    # Insert the formatting codes for the word in the segment text
                    wordlen = len(word.word)
                    text = list(segment.text)
                    text.insert(pos+wordlen, '{\c}')
                    text.insert(pos, '{\c&H9628E6&}')

                    # Create the subtitle line for the word
                    line = f"Dialogue: 0,{start_time},{end_time},{style},,0,0,0,,{''.join(text)}"
                    t.write(line+'\n')
                    pos += wordlen

                    # Set the end time of the last word to the current word's end time
                    last_end = ed
            else:
                line = f"Dialogue: 0,{format_ass_time(segment.start)},{format_ass_time(segment.end)},{style},,0,0,0,,{segment.text}"
                t.write(line+'\n')
    
    # Handling of https://github.com/guillaumekln/faster-whisper/issues/50
    except IndexError as e:
        print(e)
    
    # Close the output file
    # f.close()
    # if word_ts:
    t.close()