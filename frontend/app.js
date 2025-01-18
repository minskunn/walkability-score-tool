// Example API Response
const apiResponse = {
  proximity_to_school_and_workplace: 5,
  proximity_to_shopping_and_dining: 10,
  proximity_to_healthcare: 3,
  walkable_street_share: 40,
  green_space: 1500,
  public_transportation_accessibility: 8,
  total_walkability_score: 78,
};

// Inject Values into HTML
document.getElementById("walkability-score").textContent =
  apiResponse.total_walkability_score;
document.getElementById("proximity_to_school_and_workplace").textContent =
  apiResponse.proximity_to_school_and_workplace;
document.getElementById("proximity_to_shopping_and_dining").textContent =
  apiResponse.proximity_to_shopping_and_dining;
document.getElementById("proximity_to_healthcare").textContent =
  apiResponse.proximity_to_healthcare;
document.getElementById(
  "walkable_street_share"
).textContent = `${apiResponse.walkable_street_share}%`;
document.getElementById(
  "green_space"
).textContent = `${apiResponse.green_space} m²`;
document.getElementById("public_transportation_accessibility").textContent =
  apiResponse.public_transportation_accessibility;
