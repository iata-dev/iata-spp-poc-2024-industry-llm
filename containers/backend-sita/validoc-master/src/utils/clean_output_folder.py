def clean_output_folder():
    """Remove all files in the output folder from the previous run."""
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
