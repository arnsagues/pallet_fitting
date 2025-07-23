# save as app.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(
    page_title="Pallet Fitting",
    page_icon="🚛"
)

def visualize_stacked_packing(container_w, container_h, rect_w, rect_h, rect_count):
    orientations = [(rect_w, rect_h), (rect_h, rect_w)]

    for rw, rh in orientations:
        cols = container_w // rw
        rows = container_h // rh
        max_slots = cols * rows

        if max_slots == 0:
            continue

        full_stacks = rect_count // max_slots
        remaining = rect_count % max_slots

        fig, ax = plt.subplots()
        ax.set_xlim(0, container_w)
        ax.set_ylim(0, container_h)
        ax.grid()
        ax.set_aspect('equal')
        ax.add_patch(patches.Rectangle((0, 0), container_w, container_h,
                                       edgecolor='black', facecolor='none', linewidth=2))

        placed = 0
        for row in range(rows):
            for col in range(cols):
                x = col * rw
                y = row * rh
                stack_count = full_stacks + (1 if remaining > 0 else 0)
                if stack_count > 0:
                    rect = patches.Rectangle((x, y), rw, rh, edgecolor='blue', facecolor='lightblue')
                    ax.add_patch(rect)
                    ax.text(x + rw / 2, y + rh / 2, f"{stack_count}",
                            color='black', ha='center', va='center', fontsize=12, weight='bold')
                    placed += stack_count
                    remaining -= 1 if remaining > 0 else 0
                if placed >= rect_count:
                    break
            if placed >= rect_count:
                break

        plt.title(f"{rect_count} rolls of size {rw}x{rh} stacked in pallet {container_w}x{container_h}")
        plt.gca().invert_yaxis()
        return fig

    return None

# Streamlit UI
st.title("Pallet Roll Stacking Visualizer")
st.markdown("*Created by Arnau Sagues - July 2025*")

st.divider()

st.markdown("Enter the dimensions of the pallet and roll. Include any buffer in the desried values")
st.markdown("*All units should be in inches*")

pallet_width = st.number_input("Pallet Width", min_value=1, value=1)
pallet_length = st.number_input("Pallet Length", min_value=1, value=1)
st.badge("New")
endplate_width = st.number_input("Endplate Width (roll base)", min_value=1, value=1)
roll_length = st.number_input("Roll Length", min_value=1, value=1)
rolls_per_pallet = st.number_input("Rolls per Pallet", min_value=1, value=1)

if st.button("Visualize Stacking"):
    fig = visualize_stacked_packing(
        container_w=pallet_width,
        container_h=pallet_length,
        rect_w=endplate_width,
        rect_h=roll_length,
        rect_count=rolls_per_pallet
    )
    if fig:
        st.pyplot(fig)
    else:
        st.error("Rectangles do not fit in any orientation.")
