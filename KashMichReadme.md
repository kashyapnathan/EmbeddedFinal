# **Performance Analysis and Visualization Project**

## **Overview**
This project focuses on the comprehensive analysis of system performance metrics, including response times, bottlenecks, queue lengths, and resource utilization. By leveraging real-world datasets, we explore system behaviors under various workloads and visualize key metrics to identify inefficiencies and bottlenecks.

---


### **Response Time Data**
- **Source:** Response time data (`client_req.csv`) was obtained from production-like systems operating under simulated workloads. The dataset captures:
  - Start and end times for each request.
  - Request types (e.g., `/main.html`).
  - Total response times in milliseconds.
- **Purpose:** This data highlights variations in request handling efficiency, making it possible to identify performance bottlenecks and latency spikes.

### **Queue Metrics**
- **Source:** Queue data (`queue_length.csv`) was collected using internal system logs and middleware queue monitoring tools. It includes:
  - Real-time snapshots of queue lengths at client and server levels.
  - Derived bottleneck indicators based on queue saturation thresholds.
- **Purpose:** This dataset provides a basis for understanding the queuing behavior during high-load periods and its impact on response times.

### **CPU Data Collection**
- **SourceL macOS Activity Monitor (Built-In)**
   - **Overview**: macOS comes with Activity Monitor, which allows you to visualize CPU usage in real time.

### **Data Integrity**
- To ensure accuracy:
  - Data was pre-processed to remove anomalies and standardize timestamps.
  - Metrics were aggregated or resampled into manageable time windows for consistent analysis.

## **Key Visualizations**

The project uses real-world data to generate insightful visualizations that capture system dynamics under different conditions:

1. **Response Time Components**
   - Highlights the contribution of queuing delays and processing times to overall response latency.

2. **Time Series Analysis**
   - Examines the evolution of request rates, response times, and bottleneck events over time.

3. **Resource Utilization**
   - Explores CPU usage trends and their impact on throughput and latency.

4. **Queue Analysis**
   - Visualizes queue lengths and bottleneck periods to identify system stress points.


