function refreshSummary(summary, container) {
  const elTop = container.getBoundingClientRect().top - document.body.getBoundingClientRect().top;
  if (container.getBoundingClientRect().bottom - summary.offsetHeight < 0) {
    summary.style.position = 'absolute';
    summary.style.top = 'unset';
    summary.style.bottom = '0';
  } else if (document.documentElement.scrollTop > elTop) {
    summary.style.position = 'fixed';
    summary.style.top = '0px';
    summary.style.bottom = 'unset';
  } else {
    summary.style.position = 'absolute';
    summary.style.top = 'unset';
    summary.style.bottom = 'unset';
  }
}

const Article = {
  summary: () => {
    const container = document.getElementById('blog-content-container');
    const summary = document.getElementById('block-summary');

    refreshSummary(summary, container);
    window.addEventListener('scroll', () => {
      refreshSummary(summary, container);
    });
  },
  summaryTitles: () => {
    const summary = document.getElementById('block-summary');
    const io = new IntersectionObserver(entries => entries.forEach((item) => {
      const element = item.target;
      if (item.isIntersecting) {
        summary.querySelectorAll('a[class^="active"]').forEach(elem => elem.classList.remove('active'));
        const link = summary.querySelector(`a[href="#${element.id}"]`);
        link.classList.add('active');
      }
    }));
    document.querySelectorAll('h2[id^="titles"]').forEach(element => io.observe(element));
  },
};

const initAll = function initAllComponents() {
  Article.summary();
  Article.summaryTitles();
};

export default {
  Article,
  initAll,
};
