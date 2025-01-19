const dummyData = {
  green_space: 1500,
  proximity_to_healthcare: 3,
  proximity_to_school_and_workplace: 5,
  proximity_to_shopping_and_dining: 10,
  public_transportation_accessibility: 8,
  walkable_street_share: 40,
  total_walkability_score: 78,
};

document
  .getElementById("calculate-button")
  .addEventListener("click", function () {
    const address = document.getElementById("address-input").value;
    if (address) {
      // Inject the dummy data into the HTML
      document.getElementById("proximity_to_school_and_workplace").innerText =
        dummyData.proximity_to_school_and_workplace;
      document.getElementById("proximity_to_shopping_and_dining").innerText =
        dummyData.proximity_to_shopping_and_dining;
      document.getElementById("proximity_to_healthcare").innerText =
        dummyData.proximity_to_healthcare;
      document.getElementById("green_space").innerText = dummyData.green_space;
      document.getElementById("walkable_street_share").innerText =
        dummyData.walkable_street_share;
      document.getElementById("public_transportation_accessibility").innerText =
        dummyData.public_transportation_accessibility;

      // Change the walkability score display

      const walkabilityMessage = dummyData.total_walkability_score;
      document.getElementById("walkability-score").innerText =
        walkabilityMessage;

      // Log the address for debugging
      console.log("Address entered:", address);
    } else {
      alert("Please enter an address.");
    }
  });
