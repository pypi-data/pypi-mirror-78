import AccordionPure from './Accordion';

function createElementFromHTML(htmlString) {
  const div = document.createElement('div');
  div.innerHTML = htmlString.trim();
  return div.firstChild;
}

function animate(callbackObj, duration) {
  const requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame;
  let startTime = 0;
  let percentage = 0;
  let
    animationTime = 0;

  duration = duration * 1000 || 1000;

  const animation = function ani(timestamp) {
    if (startTime === 0) {
      startTime = timestamp;
    } else {
      animationTime = timestamp - startTime;
    }

    if (typeof callbackObj.start === 'function' && startTime === timestamp) {
      callbackObj.start();

      requestAnimationFrame(animation);
    } else if (animationTime < duration) {
      if (typeof callbackObj.progress === 'function') {
        percentage = animationTime / duration;
        callbackObj.progress(percentage);
      }

      requestAnimationFrame(animation);
    } else if (typeof callbackObj.done === 'function') {
      callbackObj.done();
    }
  };
  return requestAnimationFrame(animation);
}

function easeInOutQuad(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}


const SmoothScroll = {
  init: () => {
    const offset = 50;
    const elements = document.querySelectorAll('a[href^="#"]');
    Array.prototype.forEach.call(elements, (el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const href = el.getAttribute('href');
        const elementHref = document.getElementById(href.replace('#', ''));
        const bodyRect = document.body.getBoundingClientRect();
        const elemRect = elementHref.getBoundingClientRect();
        const posY = elemRect.top - bodyRect.top;

        if (href !== '#') {
          window.scrollTo(0, posY - offset);
        }
      }, false);
    });
  },
};


const Carousel = {
  init: () => {
    const elements = document.getElementsByClassName('carousel');
    Array.prototype.forEach.call(elements, (el) => {
      const parent = el.parentNode;
      const theme = parent.getAttribute('class').split('theme-')[1];
      const themeCorrected = theme === 'light' || theme === 'space' ? theme : 'space';
      const right = createElementFromHTML(`<img loading='lazy' class='s-icon x2 right' data-src='${Icons.right[themeCorrected]}' alt='Suivant'>`);
      const left = createElementFromHTML(`<img loading='lazy' class='s-icon x2 left' data-src='${Icons.left[themeCorrected]}' alt='Précédent'>`);
      const scrollOffset = 305;
      parent.appendChild(right);
      parent.appendChild(left);
      let scroller = 0;
      right.addEventListener('click', (e) => {
        const sequenceObj = {};
        sequenceObj.progress = (function prog(percentage) {
          el.scrollLeft = scroller + easeInOutQuad(percentage) * scrollOffset;
        });
        animate(sequenceObj, 0.5);
        scroller = el.scrollLeft;
      });
      left.addEventListener('click', (e) => {
        const sequenceObj = {};
        sequenceObj.progress = (function prog(percentage) {
          el.scrollLeft = scroller - easeInOutQuad(percentage) * scrollOffset;
        });
        animate(sequenceObj, 0.5);
        scroller = el.scrollLeft;
      });
    });
  },
};

const Clicker = {
  init: () => {
    document.addEventListener('click', (e) => {
      const elements = document.querySelectorAll('*[data-clicker-child]');
      Array.prototype.forEach.call(elements, (el) => {
        el.style.display = 'none';
      });
    });

    const elements = document.querySelectorAll('*[data-clicker]');
    Array.prototype.forEach.call(elements, (el) => {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        const child = el.querySelectorAll('*[data-clicker-child]')[0];
        const childIsVisible = child.style.visibility !== 'hidden';
        const all = document.querySelectorAll('*[data-clicker-child]');

        Array.prototype.forEach.call(all, (ell) => {
          ell.style.display = 'none';
        });
        if (childIsVisible) child.style.display = 'block';
      });
    });
  },
};

const Aside = {
  mobile: () => {
    const accordion = document.getElementById('aside-mobile');
    const accordionOpen = document.getElementById('aside-mobile-open');
    const accordionClose = document.getElementById('aside-mobile-close');

    if (accordion) {
      document.addEventListener('click', (e) => {
        accordion.style.right = '-100%';
      });

      accordionOpen.addEventListener('click', (e) => {
        e.stopPropagation();
        accordion.style.right = '0';
      });

      accordionClose.addEventListener('click', (e) => {
        e.stopPropagation();
        accordion.style.right = '-100%';
      });
    }
  },
};

const Lazy = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const element = entry.target;
        if (element.id.startsWith('slide-')) {
          // background
          element.style.backgroundImage = `url(${element.dataset.src})`;
        } else {
          // classic
          element.src = element.dataset.src;
        }
        io.unobserve(element);
      }
    }));
    document.querySelectorAll('*[loading="lazy"]').forEach(element => io.observe(element));
  },
};


const Collect = {
  init: () => {
    const collectBlock = document.getElementById('collect-block');
    const collectButton = document.getElementById('collect-btn');
    const haveAccepted = localStorage.getItem('collect');

    if (!(haveAccepted && haveAccepted === 'false')) {
      collectBlock.children[0].style.display = 'flex';
      collectButton.addEventListener('click', (e) => {
        e.stopPropagation();
        collectBlock.style.display = 'none';
        localStorage.setItem('collect', 'false');
      });
    } else {
      collectBlock.style.display = 'none';
    }
  },
};


const Accordion = {
  init: () => {
    const accordions = Array.from(document.querySelectorAll('.accordion-container'));
    if (accordions) {
      accordions.forEach((item) => {
        new AccordionPure(`#${item.id}`, {
          duration: 300,
        });
      });
    }
  },
};

const CounterUp = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((item) => {
      const element = item.target;
      if (item.isIntersecting) {
        const number = Number(element.textContent) + 1;

        let counter = 0;
        function counterJs() {
          element.innerHTML = counter.toString();
          counter += 1;
          if (counter < number) {
            setTimeout(() => {
              counterJs();
            }, 50);
          }
        }
        counterJs();
        io.unobserve(element);
      }
    }));
    document.querySelectorAll('.counter-up').forEach(element => io.observe(element));
  },
};

const Animation = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((item) => {
      const element = item.target;
      if (item.isIntersecting) {
        element.classList.add('start');
        io.unobserve(element);
      }
    }));
    document.querySelectorAll('.animation').forEach(element => io.observe(element));
  },
};

const BgSlide = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((item) => {
      const element = item.target;
      const slides = element.querySelectorAll('.bg-container-item');
      if (slides.length > 1) {
        if (item.isIntersecting) {
          const isSlider = element.classList.contains('slider');
          if (!isSlider) {
            const fSlides = Array.from(slides);
            fSlides.shift();
            let currentSlide = -1;
            let reverse = true;
            window.setInterval(() => {
              currentSlide = (currentSlide + 1) % (fSlides.length);
              reverse = currentSlide === 0 ? !reverse : reverse;
              const index = !reverse ? currentSlide : (fSlides.length - currentSlide - 1);
              fSlides[index].style.backgroundImage = `url(${fSlides[index].dataset.src})`;
              fSlides[index].classList.remove('fade-in');
              fSlides[index].classList.remove('fade-out');
              fSlides[index].classList.add(!reverse ? 'fade-in' : 'fade-out');
            }, 3000);
          } else {
            let i = 0;
            const left = element.querySelector('.left');
            const right = element.querySelector('.right');
            function resfresh() {
              for (let i = 0; i < slides.length; i++) {
                slides[i].style.backgroundImage = '';
              }
              slides[i].style.backgroundImage = `url(${slides[i].dataset.src})`;
            }
            right.addEventListener('click', (e) => {
              i = i >= slides.length - 1 ? 0 : i + 1;
              resfresh();
            });
            left.addEventListener('click', (e) => {
              i = i === 0 ? slides.length - 1 : i - 1;
              resfresh();
            });
          }
          io.unobserve(element);
        }
      }
    }));
    document.querySelectorAll('.bg-container').forEach(element => io.observe(element));
  },
};

const ReadMore = {
  init: () => {
    const elements = document.querySelectorAll('span[class="read-more"]');
    Array.prototype.forEach.call(elements, (el) => {
      const linkMore = document.createElement('a');
      linkMore.innerHTML = ' Lire la suite';
      linkMore.setAttribute('rel', 'nofollow');
      const parentDiv = el.parentNode;
      parentDiv.insertBefore(linkMore, el);
      linkMore.addEventListener('click', (e) => {
        el.style.display = 'inline';
        linkMore.remove();
      });
    });
  },
};

const initAll = function initAllComponents() {
  SmoothScroll.init();
  Carousel.init();
  Clicker.init();
  Aside.mobile();
  Lazy.init();
  Collect.init();
  Accordion.init();
  CounterUp.init();
  Animation.init();
  BgSlide.init();
  ReadMore.init();
};

export default {
  Carousel,
  SmoothScroll,
  Clicker,
  Aside,
  Lazy,
  Collect,
  Accordion,
  CounterUp,
  Animation,
  BgSlide,
  ReadMore,
  initAll,
};
