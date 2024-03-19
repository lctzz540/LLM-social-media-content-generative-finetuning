const fs = require("fs");

function removeDuplicates(array) {
  return array.filter(
    (obj, index, self) =>
      index === self.findIndex((t) => JSON.stringify(t) === JSON.stringify(obj))
  );
}

fs.readFile("./fbextracted.json", "utf8", (err, data) => {
  if (err) {
    console.error("Error reading file:", err);
    return;
  }

  try {
    const jsonData = JSON.parse(data);
    const uniqueData = removeDuplicates(jsonData);

    fs.writeFile("output.json", JSON.stringify(uniqueData, null, 2), (err) => {
      if (err) {
        console.error("Error writing file:", err);
        return;
      }
      console.log("Duplicates removed successfully.");
    });
  } catch (error) {
    console.error("Error parsing JSON:", error);
  }
});
