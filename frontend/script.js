document
  .getElementById("calculate-button")
  .addEventListener("click", function () {
    const address = document.getElementById("address-input").value;
    if (address) {
      // Send the address to the API
      fetch("https://walkability-score-tool.onrender.com/walkability", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ address: address }), // Send address to backend
      })
        .then((response) => response.json()) // Parse the JSON response
        .then((data) => {
          // Log the received data for debugging
          console.log("Received data:", data);
          // Inject the real data into the HTML
          document.getElementById(
            "proximity_to_school_and_workplace"
          ).innerText = data.details.proximity_to_school_and_workplace;
          document.getElementById(
            "proximity_to_shopping_and_dining"
          ).innerText = data.details.proximity_to_shopping_and_dining;
          document.getElementById("proximity_to_healthcare").innerText =
            data.details.proximity_to_healthcare;
          document.getElementById("green_space").innerText =
            data.details.green_space;
          document.getElementById("walkable_street_share").innerText =
            data.details.walkable_street_share;
          document.getElementById(
            "public_transportation_accessibility"
          ).innerText = data.details.public_transportation_accessibility;

          // Change the walkability score display
          const walkabilityMessage = data.walkability_score;
          document.getElementById("walkability-score").innerText =
            walkabilityMessage;

          document.querySelector(".metrics").style.display = "block";

          // Log the address for debugging
          console.log("Address entered:", address);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
          alert("There was an error fetching data. Please try again later.");
        });
    } else {
      alert("Please enter an address.");
    }
  });
