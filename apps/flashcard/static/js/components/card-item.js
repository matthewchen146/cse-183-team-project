export default {
  props: {
    info: {
      type: Object,
      default: {},
    },
    cardIndex: {
      type: Number,
      required: true,
    },
  
  },
  methods: {
    toggleCard() {
      this.info.isFront = !this.info.isFront;
    
    },
    
  },
  data() {
    if (this.info.isFront === undefined) {
      this.info.isFront = true;
    }
    return {
      cardUrl: `edit/${this.info.deck_id}`,
    };
  },
  template: await loadHtml('./static/js/components/card-item-template.html')
};
