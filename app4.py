import streamlit as st
from ollama import Client
import os
import re
import zipfile
import shutil

# ================================
# Initialize Ollama client
# ================================
client = Client()

# ================================
# Streamlit UI Setup
# ================================
st.set_page_config(page_title="AutoDev – Full Project Generators", page_icon="💻", layout="wide")
st.title("💻 AutoDev — Full Project Generator + Chat + File Builder")

# ================================
# Session State
# ================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "project_folder" not in st.session_state:
    st.session_state.project_folder = "generated_project"

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================================
# Chat Input
# ================================
prompt = st.chat_input("💬 Enter your request (Generate code, modify code, create project, etc.)")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare context
    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    # AI Response Area
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Generating...")

        try:
            # ================================
            # Call Ollama model
            # ================================
            response = client.chat(
                model="llama3",
                messages=[
                    {"role": "system", "content": "You are an AI that generates full coding projects with folders, files, and documentation."},
                    {"role": "user", "content": context}
                ]
            )

            reply = response["message"]["content"]
            placeholder.markdown(reply)

            # Save reply to session state
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            placeholder.markdown(f"⚠️ Error: {e}")


# ============================================================
# 🔽 PHASE 2 — FILE GENERATION
# Extract code blocks and save to files
# ============================================================
st.subheader("📂 Generate Project Files")

if st.button("Generate Files From AI Output"):
    folder = st.session_state.project_folder

    # Clean old folder if exists
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    last_reply = st.session_state.messages[-1]["content"]

    # Regex for code blocks
    blocks = re.findall(r"```(.*?)```", last_reply, re.DOTALL)

    file_counter = 1
    created_files = []

    for block in blocks:
        # Detect language
        parts = block.split("\n", 1)
        lang = parts[0].strip()
        code = parts[1] if len(parts) > 1 else ""

        ext = {
            "python": "py",
            "py": "py",
            "javascript": "js",
            "js": "js",
            "html": "html",
            "css": "css",
            "java": "java",
        }.get(lang.lower(), "txt")

        filename = f"file_{file_counter}.{ext}"
        filepath = os.path.join(folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        created_files.append(filename)
        file_counter += 1

    st.success(f"Created {len(created_files)} files inside `{folder}/`")
    st.write(created_files)


# ============================================================
# 🔽 PHASE 3 — AUTO requirements.txt
# ============================================================
st.subheader("📘 Auto-Generate requirements.txt")

if st.button("Create requirements.txt"):
    folder = st.session_state.project_folder

    requirements = set()

    # Scan for imports in all .py files
    for f in os.listdir(folder):
        if f.endswith(".py"):
            content = open(os.path.join(folder, f), "r", encoding="utf-8").read()
            matches = re.findall(r"import (\w+)|from (\w+)", content)
            for m in matches:
                pkg = m[0] or m[1]
                requirements.add(pkg)

    req_path = os.path.join(folder, "requirements.txt")
    with open(req_path, "w") as f:
        for pkg in requirements:
            f.write(pkg + "\n")

    st.success("requirements.txt generated!")
    st.code("\n".join(requirements))


# ============================================================
# 🔽 PHASE 4 — ZIP Project Folder
# ============================================================
st.subheader("📦 Download Project as ZIP")

zip_path = "project.zip"

if st.button("Zip Project Folder"):
    folder = st.session_state.project_folder

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for f in files:
                zipf.write(os.path.join(root, f),
                           os.path.relpath(os.path.join(root, f), folder))

    st.success("Project zipped successfully!")

    with open(zip_path, "rb") as fp:
        st.download_button("⬇ Download ZIP", fp, file_name="project.zip")


# ============================================================
# 🔽 PHASE 6 — README Generator
# ============================================================
st.subheader("📄 Auto-Generate README.md")

if st.button("Generate README.md"):
    folder = st.session_state.project_folder

    template = f"""
# 🚀 Auto-Generated Project

This project was generated using **AutoDev AI Generator**.

## 📌 Description
{st.session_state.messages[-1]["content"]}

## 📂 Folder Structure """
