const currentDate = new Date();

// Format the date as "Month Day, Year" (e.g., "November 24, 2023")
const formattedDate = currentDate.toLocaleDateString("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
});

// Set the form title with the formatted date
const formTitle = document.getElementById("form-title");
formTitle.textContent = `${formattedDate}`;
