/*global module:false*/
module.exports = function (grunt) {

    'use strict';

    // Project configuration.
    grunt.initConfig({
        vars: {
            src_js_dir: 'static/js/',
            src_js: '*.js'
        },
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            gruntfile: ['Gruntfile.js'],
            js: ['<%= vars.src_js_dir %><%= vars.src_js %>', '<%= vars.src_js_dir %>demo/<%= vars.src_js %>']
        },
        watch: {
            gruntfile: {
                files: '<%= jshint.gruntfile %>',
                tasks: ['jshint:gruntfile']
            },
            js: {
                files: '<%= jshint.js %>',
                tasks: ['jshint:js']
            }
        }
    });

    // Default task
    grunt.registerTask('default', ['jshint']);

    // Plugin tasks
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
