""""
Name: Shipping and Receiving Visualizer 
Author: Arnau Sagues 
Date: 07/23/2025
"""

"""
Sec. 1: Import libraries 
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math 

"""
Page UI: Title
"""
# Page config
st.set_page_config(
    page_title="Pallet Fitting",
    page_icon="🚛"
)

st.title("Pallet Roll Stacking Visualizer")
st.caption("_Created by Arnau Sagues - July 2025_")

st.divider()

"""
Sec. 2: Visulazing pallets and rolls 
"""
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

# User input #
st.markdown("Enter the dimensions of the pallet and roll. Include any buffer in the desried values")
st.markdown("*All units should be in inches*")

pallet_width = st.number_input("Pallet Width", min_value=1, value=1)
pallet_length = st.number_input("Pallet Length", min_value=1, value=1)
endplate_width = st.number_input("Endplate Width (roll base)", min_value=1, value=1)
st.caption("This should be the side of the endplate that will be in contact with the pallet")
roll_length = st.number_input("Roll Length", min_value=1, value=1)
rolls_per_pallet = st.number_input("Rolls per Pallet", min_value=1, value=1)

# Run the script #
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

"""
Sec. 3: Pallet packing into a container
"""
st.divider()
st.title("Container Pallet Fitting Visualizer")

# User input #
container_w = st.number_input("Container Width", min_value=1, value=100, key="cont_w")
container_l = st.number_input("Container Length", min_value=1, value=200, key="cont_l")

pallet_count = st.number_input("Number of Pallet Types", min_value=1, max_value=5, value=1)

pallets = []

for i in range(pallet_count):
    st.subheader(f"Pallet Type {i+1}")
    pw = st.number_input(f"Pallet {i+1} Width", min_value=1, value=40, key=f"pw_{i}")
    pl = st.number_input(f"Pallet {i+1} Length", min_value=1, value=48, key=f"pl_{i}")
    qty = st.number_input(f"Pallet {i+1} Quantity", min_value=1, value=10, key=f"qty_{i}")
    pallets.append((pw, pl, qty))

def visualize_pallet_packing(container_w, container_l, pallets):
    import math

    fig, ax = plt.subplots()
    ax.set_xlim(0, container_w)
    ax.set_ylim(0, container_l)
    ax.set_aspect('equal')
    ax.grid()
    ax.add_patch(patches.Rectangle((0, 0), container_w, container_l,
                                   edgecolor='black', facecolor='none', linewidth=2))

    color_map = ['lightgreen', 'lightred', 'lightblue', 'lightyellow', 'violet']
    legend_handles = []

    # Track occupied area: initialize with False
    occupied_map = [[None for _ in range(container_w)] for _ in range(container_l)]

    def is_area_free(x, y, w, h):
        if x + w > container_w or y + h > container_l:
            return False
        for i in range(y, y + h):
            for j in range(x, x + w):
                if occupied_map[i][j] is not None:
                    return False
        return True

    def occupy_area(x, y, w, h, idx):
        for i in range(y, y + h):
            for j in range(x, x + w):
                occupied_map[i][j] = idx

    for idx, (pw, pl, qty) in enumerate(pallets):
        best_orientation = None
        best_fit = 0
        best_positions = []

        # Try both orientations
        for (tw, tl) in [(pw, pl), (pl, pw)]:
            positions = []
            for y in range(0, container_l - tl + 1, tl):
                for x in range(0, container_w - tw + 1, tw):
                    if is_area_free(x, y, tw, tl):
                        positions.append((x, y, tw, tl))
            if len(positions) > best_fit:
                best_fit = len(positions)
                best_orientation = (tw, tl)
                best_positions = positions

        if not best_positions:
            continue

        stacks_per_slot = qty // len(best_positions)
        extra_stacks = qty % len(best_positions)

        for i, (x, y, tw, tl) in enumerate(best_positions):
            if i * stacks_per_slot + min(i, extra_stacks) >= qty:
                break  # stop once we've placed all pallets

            occupy_area(x, y, tw, tl, idx)

            count = stacks_per_slot + (1 if i < extra_stacks else 0)
            rect = patches.Rectangle((x, y), tw, tl,
                                     edgecolor='black', facecolor=color_map[idx % len(color_map)])
            ax.add_patch(rect)
            ax.text(x + tw / 2, y + tl / 2, str(count), color='black',
                    ha='center', va='center', fontsize=10, weight='bold')

        legend_patch = patches.Patch(color=color_map[idx % len(color_map)],
                                     label=f"Pallet {idx+1} ({pw}x{pl})")
        legend_handles.append(legend_patch)

    plt.title("Pallet Stack Counts in Container")
    plt.gca().invert_yaxis()
    ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1.0, 0.5))
    return fig

# Run the function #
if st.button("Visualize Pallet Fit in Container"):
    fig = visualize_pallet_packing(container_w, container_l, pallets)
    if fig:
        st.pyplot(fig)
    else:
        st.error("Unable to fit pallets in the container.")
