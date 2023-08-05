const CollapseBlock = {
  init: () => {
    $('#body-list').children().each(function col() {
      const header = $(this).find('.cms-block-head').first().get(0);
      const content = $(this).find('.c-sf-block__content-inner').first().get(0);
      content.style.display = 'none';
      header.addEventListener('click', (e) => {
        e.preventDefault();
        if (content.style.display === 'block') {
          content.style.display = 'none';
        } else {
          content.style.display = 'block';
        }
      }, false);
    });
  },
};

const initAll = function initAllComponents() {
  CollapseBlock.init();
};

export default {
  CollapseBlock,
  initAll,
};
