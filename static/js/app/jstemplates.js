this["KNET"] = this["KNET"] || {};
this["KNET"]["templates"] = this["KNET"]["templates"] || {};

this["KNET"]["templates"]["no_stories_msg"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return " my-stories";
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <p>\n      You don't have any stories.\n      ";
  stack1 = helpers['if'].call(depth0, depth0.profile_url, {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </p>\n  ";
  return buffer;
  }
function program4(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n        Send current or former students to:\n        <span class=\"share-profile-link\">";
  if (stack1 = helpers.profile_url) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.profile_url; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1)
    + "</span>\n      ";
  return buffer;
  }

function program6(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <p>\n      Be the first to leave a story";
  stack1 = helpers['if'].call(depth0, depth0.teacher_name, {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += ".\n    </p>\n  ";
  return buffer;
  }
function program7(depth0,data) {
  
  var buffer = "", stack1;
  buffer += " for ";
  if (stack1 = helpers.teacher_name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = depth0.teacher_name; stack1 = typeof stack1 === functionType ? stack1.apply(depth0) : stack1; }
  buffer += escapeExpression(stack1);
  return buffer;
  }

  buffer += "<div class=\"no-stories-message";
  stack1 = helpers['if'].call(depth0, depth0.my_profile, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n  ";
  stack1 = helpers['if'].call(depth0, depth0.my_profile, {hash:{},inverse:self.program(6, program6, data),fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n";
  return buffer;
  });