from psychopy import sound,core,event

def playAudio(target, env):
    ## Must convert wav files to 24 Bit, 48000 Hz, Default https://onlineaudioconverter.com/#
    audio_path = 'audio/'

    if target == "resp":
        # Play sound to indicate time to respond
        #snddata = sound.Sound(value=300, secs=0.5, sampleRate=env["sampleRate"])
        snddata = sound.Sound(value=300, secs=0.5, stereo=True, sampleRate=env["sampleRate"])
        snddata.play()
        core.wait(0.5)

    elif target == "warning":
        # Play warning audio file
        warning_sound = sound.Sound(audio_path + 'warning.wav')
        warning_sound.play()
        core.wait(warning_sound.getDuration()) #wait until audio ends

    if target == "break":
        # Play break audio file
        break_sound = sound.Sound(audio_path + 'break.wav')
        #print(break_sound.sampleRate)
        break_sound.play()
        core.wait(break_sound.getDuration())

    elif target == "outro":
        # Play congrats audio file
        congrats_sound = sound.Sound(audio_path + 'congrats.wav')
        congrats_sound.play()
        core.wait(congrats_sound.getDuration())