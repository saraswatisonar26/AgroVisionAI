const imageInput = document.getElementById("image");
const fileName = document.getElementById("file-name");

console.log("Script Loaded");

if (imageInput && fileName) {

    imageInput.addEventListener("change", function () {

        console.log("File Selected");

        if (this.files.length > 0) {
            fileName.textContent = "✅ " + this.files[0].name;
        } else {
            fileName.textContent = "No image selected";
        }

    });

}