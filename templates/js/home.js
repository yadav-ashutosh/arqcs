const getDataButton = document.getElementById("getDataButton");
const dataDiv = document.getElementById("dataDiv");

getDataButton.addEventListener("click", async () => {
  try {
    const response = await fetch("/get_data", {
      method: "POST",
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data);
      dataDiv.innerText = data.message; // Update the div with received data
    } else {
      dataDiv.innerText = "Error fetching data";
      dataDiv.style.color = "red";
    }
  } catch (error) {
    console.error("An error occurred:", error);
    dataDiv.innerText = "Error fetching data";
  }
});

const subscriptions = document.querySelector(".list-group");
const subscribeButton = document.getElementById("subscribeButton");

subscribeButton.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/get_data", {
      method: "GET",
    });
  } catch (error) {
    console.error("An error occurred while recieving subscribed users:", error);
  }
});
