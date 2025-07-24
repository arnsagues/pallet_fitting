Pallet and Shipping Container Visualizer
========================================

Overview:
---------
This Streamlit app helps visualize how pallets or rolls are stacked within pallets or shipping containers. 
It supports multiple pallet types, automatic orientation selection, and visual stack counts to optimize layout planning for logistics, warehousing, and shipping.

Main Features:
--------------
1. **Rolls in Pallets**:
   - Enter pallet dimensions and roll dimensions.
   - Visualize the stacking of rolls in the most optimal orientation.
   - Shows number of stacked rolls per slot.

2. **Pallets in Containers**:
   - Enter shipping container dimensions.
   - Add one or more pallet types with dimensions and quantities.
   - App auto-orients each pallet type to best fit the available space.
   - Ensures pallet types are stacked only with their own kind.
   - Displays the number of stacked pallets per placement.
   - Adds a legend showing which color corresponds to which pallet type.

How to Use:
-----------
1. **Launch the app via Streamlit**:
`streamlit run app.`


2. **Roll Stacking Section**:
- Input pallet width, length, roll width (endplate), roll length, and number of rolls.
- Click "Visualize Stacking" to see how rolls stack on a pallet.

3. **Container Loading Section**:
- Input container width and length.
- Specify the number of pallet types.
- For each pallet type, input width, length, and total quantity.
- Click "Visualize Pallet Fit in Container" to see the layout.

Technical Notes:
----------------
- Layout logic is greedy and fills the container from top-left to bottom-right.
- Stack counts are calculated based on how many pallets can be placed in each slot.
- Legend is placed outside the plot for clarity.

Requirements:
-------------
- Python 3.7+
- streamlit
- matplotlib

Install dependencies:
---------------------
`pip install streamlit matplotlib`


Author:
-------
Arnau Sagues
