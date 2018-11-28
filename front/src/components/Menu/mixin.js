import {findComponentUpward, findComponentsUpward} from '../../utils/assist';
export default {
  data() {
    return {
      menu: findComponentUpward(this, 'Menu')
    };
  },
  computed: {
    hasParentSubmenu() {
      return !!findComponentUpward(this, 'Submenu');
    },
    parentSubmenuNum() {
      return findComponentsUpward(this, 'Submenu').length;
    },
    mode() {
      return this.menu.mode;
    }
  },
  methods: {
    showTitle(item) {
      return item.name
    },
    showChildren(item) {
      if (item.children && item.children.length !== 0) {
        for (let c in item.children) {
          if (item.children[c].meta) {
            if (item.children[c].meta.visible) {
              return true
            }
          }
        }
        return false
      }
    }
  }
}



