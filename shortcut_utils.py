import streamlit.components.v1 as components
import json
import streamlit as st


def add_shortcuts(**shortcuts: str) -> None:
    """Replacement for streamlit_shortcuts.add_shortcuts that prevents multiple listener buildup."""
    assert shortcuts, "No shortcuts provided"

    js = (
        """
<script>
const doc = window.parent.document;

// Remove old shortcut listener if it exists
if (window.__streamlitShortcutsListener) {
    doc.removeEventListener('keydown', window.__streamlitShortcutsListener, true);
}

// Define and store new listener
window.__streamlitShortcutsListener = function(e) {
"""
        + f"    const shortcuts = {json.dumps(shortcuts)};\n"
        + """
    for (const [key, shortcut] of Object.entries(shortcuts)) {

        const isTyping = (
                    e.target.tagName === "TEXTAREA" ||
                    (e.target.tagName === "INPUT" && e.target.type === "text")
                );
        if (isTyping) {
            // Ignore shortcuts when typing in text inputs
            return;
        }
        const parts = shortcut.toLowerCase().split('+');
        const hasCtrl = parts.includes('ctrl');
        const hasAlt = parts.includes('alt');
        const hasShift = parts.includes('shift');
        const hasMeta = parts.includes('meta') || parts.includes('cmd');
        const mainKey = parts.find(p => !['ctrl','alt','shift','meta','cmd'].includes(p));

        if (hasCtrl === e.ctrlKey &&
            hasAlt === e.altKey &&
            hasShift === e.shiftKey &&
            hasMeta === e.metaKey &&
            e.key.toLowerCase() === mainKey) {

            e.preventDefault();

            const el =
                doc.querySelector(`.st-key-${key} button`) ||
                doc.querySelector(`.st-key-${key} input`) ||
                doc.querySelector(`[data-testid="${key}"]`) ||
                doc.querySelector(`button:has([data-testid="baseButton-${key}"])`) ||
                doc.querySelector(`[aria-label="${key}"]`);

            if (el) {
                const classOK = el.classList.contains("shortcut-enabled");
                const attrOK = el.getAttribute("data-shortcut") === "true";
                const activeEl = document.activeElement;

                

                if ((classOK || attrOK) && !isTyping) {
                    console.log(`Shortcut triggered: ${key} -> ${shortcut}`);
                    console.log("Active element:", activeEl);
                    console.log("Event target:", e.target.tagName);
                    el.click();
                    el.focus();
                }
            }
        }
    }
};

doc.addEventListener('keydown', window.__streamlitShortcutsListener, true);
</script>
"""
    )
    components.html(js, height=0, width=0)


def shortcut_button(
    label: str, shortcut=None, hint: bool = True, **kwargs
) -> bool:  # noqa: FBT002 (boolean positional arg)
    """Streamlit button with a keyboard shortcut.

    Args:
        label: Button text (can be empty string)
        shortcut: Keyboard shortcut like 'ctrl+s', 'alt+shift+d', 'meta+k', or just 'x'
        hint: Show shortcut hint in button label (default: True)
        **kwargs: All other st.button args (key, type, disabled, use_container_width, etc.)

    Returns:
        bool: True if button was clicked (same as st.button)
    """
    assert label is not None, "Button label cannot be None"
    # assert shortcut, "Shortcut parameter is required"

    # Generate key if not provided
    if "key" not in kwargs:
        kwargs["key"] = f"btn_{hash(label + shortcut) % 10000000}"

    # Add hint to label if requested
    button_label = (
        f"{label} `{shortcut}`" if hint and label and (shortcut is not None) else label
    )

    # Create button WITHOUT hint parameter
    clicked = st.button(button_label, **kwargs)

    # Add the shortcut
    if shortcut is not None:
        add_shortcuts(**{kwargs["key"]: shortcut})
        # Add an html class to mark the button as a shortcut-enabled element
        components.html(
            f"""
        <script>
        const el = window.parent.document.querySelector('.st-key-{kwargs["key"]} button');"""
            + """
        if (el) {{
            el.classList.add("shortcut-enabled");
            el.setAttribute("data-shortcut", "true");
        }}
        </script>
        """,
            height=0,
        )
    return clicked
