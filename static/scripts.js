const fileInput = document.querySelector('#file');
const scrollButton = document.querySelector('button');
const targetSection = document.querySelector('form');
const output = document.querySelector('.output-p');
const loadingAnimation = document.getElementById("loading-animation");

fileInput.addEventListener('change', function() {
  const fileName = this.files[0].name;

  const fileNameDisplay = document.querySelector('#file-name');
  fileNameDisplay.textContent = `File selected : ${fileName}` 
});

window.addEventListener('load',(()=>{
    if(output.textContent == "" || output.textContent == "[]"){
        output.textContent = "Output will be displayed here"
    }
    loadingAnimation.style.display = "none";
    if(screen.width < 1300){
      targetSection.scrollIntoView({ behavior: 'smooth' });
    }
}))

document.querySelector('button').addEventListener('click',()=>{
  loadingAnimation.style.display = "flex"
})
