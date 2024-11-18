import streamlit as st

# Define the calculate_bandwidth function
def calculate_bandwidth(image_size, throughput, throughput_time_unit, throughput_type, rejection_rate, num_machines, output_unit, image_size_unit):
    # Convert image size to MB if needed
    if image_size_unit == "KB":
        image_size_mb = image_size / 1024
    elif image_size_unit == "GB":
        image_size_mb = image_size * 1024
    elif image_size_unit == "TB":
        image_size_mb = image_size * 1024 * 1024
    else:
        image_size_mb = image_size  # Assume MB if no conversion needed

    # Calculate throughput per month
    if throughput_time_unit == "per hour":
        throughput_per_month = throughput * 24 * 30  # 30 days per month
    elif throughput_time_unit == "per year":
        throughput_per_month = throughput / 12  # Convert yearly throughput to monthly
    else:
        throughput_per_month = throughput  # Monthly throughput directly provided

    # Adjust for throughput type (Per Machine or All Machines)
    if throughput_type == "Per Machine":
        total_throughput = throughput_per_month * num_machines
    else:
        total_throughput = throughput_per_month

    # Total data transferred per month in Megabits
    total_data_megabits = total_throughput * image_size_mb * 8  # 1 MB = 8 Megabits

    # Convert total data to bandwidth (per second) in Mbps
    seconds_in_month = 30 * 24 * 60 * 60  # 30 days per month
    total_bandwidth_mbps = total_data_megabits / seconds_in_month

    # Convert bandwidth to the selected unit
    if output_unit == "Kbps":
        total_bandwidth = total_bandwidth_mbps * 1000
    elif output_unit == "Gbps":
        total_bandwidth = total_bandwidth_mbps / 1000
    else:
        total_bandwidth = total_bandwidth_mbps  # Default is Mbps

    # Bandwidth per X-ray Machine
    bandwidth_per_machine = total_bandwidth / num_machines

    # Rejected bags based on rejection rate
    rejected_bags = total_throughput * (rejection_rate / 100)

    # Total bags from site (excluding rejected bags)
    total_bags_from_site = total_throughput - rejected_bags

    return total_bandwidth, bandwidth_per_machine, rejected_bags, total_bags_from_site

# Streamlit UI with updated styles
st.markdown(
    """
    <style>
    /* Custom CSS for styling */
    .stApp {
        background: linear-gradient(to bottom right, black, #3E54AC);
        padding: 0;
        margin: 0;
        width: 100vw;
        height: 100vh;
        position: relative;
    }
    h1 {
        text-align: center;
        color: #91D8E4;
        font-weight: bold;
        font-size: 36px;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
        margin-top: 100px;
    }
    .company-name {
        position: absolute;
        top: 30px;
        left: 30px;
        font-size: 40px;
        font-weight: bold;
    }
    .company-name .Smiths {
        color: #B9F3FC;
    }
    .company-name .Detection {
        color: #ECF9FF;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #fff;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;  /* Larger font size for inputs */
        width: 250px;
        color: #333;  /* Dark text for better readability */
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stMultiselect label {
        color: #FFFFFF;  /* White color for input headings */
        font-size: 20px;  /* Increased font size for input labels */
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stSelectbox, .stMultiselect {
        background-color: transparent;  /* Transparent background to match page background */
        border: none;  /* Remove borders */
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;  /* Larger font size for dropdowns */
        width: 150px;  /* Set width to match image size input box */
        color: white;  /* White text for better visibility */
    }
    .stSelectbox div, .stMultiselect div {
        background-color: transparent;  /* Transparent dropdown options background */
        color: white;  /* White text for dropdown options */
    }
    .stButton button {
        background-color: #BAD7E9;  /* New button color (tomato red) */
        color: white;
        font-size: 18px;
        border-radius: 12px;
        padding: 15px;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #FCFFE7;  /* Darker tomato color when hovered */
    }
    .stNumberInput input {
        padding-right: 40px;  /* Add padding to the right so the + and - buttons don't overlap */
    }
    </style>
    """, unsafe_allow_html=True
)

# Display company name
st.markdown("<div class='company-name'><span class='Smiths'>Smiths</span> <span class='Detection'>Detection</span></div>", unsafe_allow_html=True)

# Display the app name
st.markdown("<h1>Bandwidth Analyzer</h1>", unsafe_allow_html=True)

# Inputs for image size and throughput
col1, col2 = st.columns([3, 1])
with col1:
    image_size_input = st.number_input("Enter Image Size (in MB)", min_value=0.0, step=0.1)
with col2:
    image_size_unit = st.selectbox("Select Unit", ["KB", "MB", "GB", "TB"])

# Throughput section
col3, col4, col5 = st.columns([1, 1, 1])
with col3:
    throughput_input = st.number_input("Enter Throughput", min_value=0.0, step=1.0)
with col4:
    throughput_time_unit = st.selectbox("Select Throughput Time Unit", ["per hour", "per month", "per year"], index=1)
with col5:
    throughput_type = st.selectbox("Is Throughput Per Machine or All Machines?", ["Per Machine", "All Machines"], index=1)

# Input for the number of X-ray machines
num_machines = st.number_input("Enter Number of X-ray Machines", min_value=1, step=1)

# Rejection rate input
st.markdown("<h3 style='color: white; font-size: 20px;'>Enter Rejection Rate (%)</h3>", unsafe_allow_html=True)
rejection_rate = st.number_input("", min_value=0.0, max_value=100.0, step=0.1)

# Output unit
output_unit = st.selectbox("Select Output Unit", ["Mbps", "Kbps", "Gbps"], index=0)

# Calculate button
if st.button("🔍 Calculate"):
    # Get the inputs and call the calculate_bandwidth function
    bandwidth, bandwidth_per_machine, rejected_bags, total_bags_from_site = calculate_bandwidth(
        image_size_input, throughput_input, throughput_time_unit, throughput_type, rejection_rate, num_machines, output_unit, image_size_unit
    )

    # Display results
    st.markdown('<h3 style="color:white;">Results</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:white; font-size:16px;"><strong>Total bandwidth required:</strong> {bandwidth:.4f} {output_unit}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:white; font-size:16px;"><strong>Bandwidth required per X-ray Machine (Lane):</strong> {bandwidth_per_machine:.4f} {output_unit}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:white; font-size:16px;"><strong>Total rejected bags:</strong> {rejected_bags:.4f} bags</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:white; font-size:16px;"><strong>Total bags from site:</strong> {total_bags_from_site:.4f} bags</p>', unsafe_allow_html=True)
