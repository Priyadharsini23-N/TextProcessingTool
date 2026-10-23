
import streamlit as st
import zlib
import re
from spellchecker import SpellChecker

st.title("Text Processing Tool")
st.write("Check spelling, correct mistakes, and compress text files.")

# FILE UPLOAD
uploaded_file = st.file_uploader(
    "Upload a text file",
    type=["txt"]
)

if uploaded_file is not None:

    text = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )

    st.success("File uploaded successfully!")

    st.subheader("Original Text")
    st.text_area("Uploaded file content", text, height=150)

    # SPELLING CHECKER
    st.divider()
    st.subheader("1. Spelling Checker")

    if st.button("Check Spelling"):

        spell = SpellChecker()
        words = re.findall(r"[A-Za-z]+", text)
        unique_words = set(word.lower() for word in words)
        mistakes = spell.unknown(unique_words)

        if mistakes:
            st.warning("Possible spelling mistakes found:")

            for word in sorted(mistakes):
                correction = spell.correction(word)
                st.write(f"{word} → {correction}")
        else:
            st.success("No spelling mistakes found!")

    # SPELLING CORRECTION
    st.divider()
    st.subheader("2. Correct Spelling")

    if st.button("Correct Spelling"):

        spell = SpellChecker()
        corrected_text = text

        words = set(re.findall(r"[A-Za-z]+", text))

        for word in words:
            if word.lower() in spell.unknown([word.lower()]):
                correction = spell.correction(word.lower())

                if correction:
                    corrected_text = re.sub(
                        r"\b" + re.escape(word) + r"\b",
                        lambda match: (
                            correction.capitalize()
                            if match.group().istitle()
                            else correction.upper()
                            if match.group().isupper()
                            else correction
                        ),
                        corrected_text,
                        flags=re.IGNORECASE
                    )

        st.text_area(
            "Corrected text",
            corrected_text,
            height=150
        )

        st.download_button(
            "Download Corrected Text",
            data=corrected_text.encode("utf-8"),
            file_name="corrected_text.txt",
            mime="text/plain"
        )

    # TEXT COMPRESSION
    st.divider()
    st.subheader("3. Text Compression")

    if st.button("Compress File"):

        original_data = text.encode("utf-8")
        compressed_data = zlib.compress(original_data)

        original_size = len(original_data)
        compressed_size = len(compressed_data)

        st.write("Original size:", original_size, "bytes")
        st.write("Compressed size:", compressed_size, "bytes")

        if original_size > 0:
            reduction = (
                (original_size - compressed_size)
                / original_size
            ) * 100

            st.write(
                "Size reduction:",
                round(reduction, 2),
                "%"
            )

        st.download_button(
            "Download Compressed File",
            data=compressed_data,
            file_name="compressed_text.zlib",
            mime="application/octet-stream"
        )

        st.download_button(
            "Download Original Text",
            data=original_data,
            file_name="original_text.txt",
            mime="text/plain"
        )




