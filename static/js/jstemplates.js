this["KNET"] = this["KNET"] || {};
this["KNET"]["templates"] = this["KNET"]["templates"] || {};

this["KNET"]["templates"]["no_stories_msg"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div class=\"no-stories-message\">\n  <p>You have no stories.</p>\n</div>\n";
  });