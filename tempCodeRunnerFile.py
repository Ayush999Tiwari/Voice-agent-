
    model = get_model()
    logger.info("Transcribing...")
    segments, info = model.transcribe(
        str(audio_path),