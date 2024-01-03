const aboutUsCardAdvantages = document.querySelector('.advantages .card-body');
const aboutUsIMGSLink = "/static/main/img/aboutUs-page/advantage-list/";

const advantagesList = [
  {
    title: "ПОЛНОСТЬЮ ОТВЕТСТВЕННЫЙ",
    img: "Group1.png",
    description: "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In eleifend suscipit enim, eu commodo neque molestie vitae."
  },
  {
    title: "НЕОГРАНИЧЕННЫЕ ВАРИАНТЫ",
    img: "Group2.png",
    description: "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In eleifend suscipit enim, eu commodo neque molestie vitae."
  },
  {
    title: "бесплатного участия",
    img: "Group3.png",
    description: "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In eleifend suscipit enim, eu commodo neque molestie vitae."
  },
  {
    title: "электронная коммерция",
    img: "Group4.png",
    description: "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In eleifend suscipit enim, eu commodo neque molestie vitae."
  },
  {
    title: "бесплатное образование",
    img: "Group5.png",
    description: "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In eleifend suscipit enim, eu commodo neque molestie vitae."
  },
  {
    title: "ПОДДЕРЖИВАТЬ",
    img: "Group6.png",
    description: "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In eleifend suscipit enim, eu commodo neque molestie vitae."
  },
]

function generateAdvantagesList(advantagesList) {
  advantagesList.map((cardInfo) => {
    let advantageCard = `
         <div class="card mb-3 col-12 col-lg-4 col-xl-3">
                <div class="col g-0">
                  <div class="row-md-3 d-flex">
                    <img src="${aboutUsIMGSLink}${cardInfo.img}" class="img-fluid rounded-start" alt="${cardInfo.img}">
                    <h3 class="card-title">${cardInfo.title}</h3>
                  </div>
                  <div class="col-md-12">
                    <div class="card-body">
                      <p class="card-text">${cardInfo.description}</p>
                    </div>
                  </div>
                </div>
              </div> 
        `
    aboutUsCardAdvantages.insertAdjacentHTML("beforeend", advantageCard)
  })
}

generateAdvantagesList(advantagesList)


$('.slick-slider').slick({
  dots: true,
  infinite: true,
  speed: 300,
  slidesToShow: 4,
  slidesToScroll: 4,
  autoplay: true,
  autoplaySpeed: 2000,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }

  ]
});

const aboutUsPersonIMGs = document.querySelector('.aboutUs-page-experts-imgList')
const aboutUsExportInfo = document.querySelector('.aboutUs-page-exportInfo')

function generatePersonalInfo(img, name, jobTitle, detail) {

  return `
  <div id="person1" class="card mb-3" >
  <div class="row g-0">
    <div class="col-md-4 expert_card_top">
      <img src="${img}" class="img-fluid rounded-start" alt="${name}">
      <h5 class="card-title">${jobTitle}</h5>
    </div>
    <div class="col-md-8">
      <div class="card-body">
        <h4 class="card-title">${name}</h4>
        <p class="card-text">${detail}</p>
        <!--<p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>-->
      </div>
    </div>
  </div>
  </div>
  `
}

const firstIMG = aboutUsPersonIMGs.querySelector('.slick-track').firstElementChild


aboutUsExportInfo.innerHTML = generatePersonalInfo(
  firstIMG.src,
  firstIMG.getAttribute("data-name"),
  firstIMG.getAttribute("data-jobtitle"),
  firstIMG.getAttribute("data-info")
)

aboutUsPersonIMGs.addEventListener("mouseover", e => {
  console.log(e.target.getAttribute("data-person"));
  if (e.target.getAttribute("data-person")) {
    aboutUsExportInfo.innerHTML = generatePersonalInfo(
      e.target.src,
      e.target.getAttribute("data-name"),
      e.target.getAttribute("data-jobtitle"),
      e.target.getAttribute("data-info")
    )
  }
})

function myFunction() {
  var dots = document.getElementById("dots");
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("myBtn");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more";
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less";
    moreText.style.display = "inline";
  }
}


