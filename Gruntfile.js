/*global module:false*/
module.exports = function (grunt) {

    'use strict';

    // Project configuration.
    grunt.initConfig({
        vars: {
            src_py_dir: 'knet/',
            src_templates_dir: 'templates/',
            src_js_dir: 'static/js/',
            js_tests_dir: 'jstests/',
            src_js_templates: 'jstemplates/*.hbs',
            dest_js_templates: '<%= vars.src_js_dir %>jstemplates.js'
        },
        pkg: grunt.file.readJSON('package.json'),
        qunit: {
            options: {
                coverage: {
                    src: ['<%= jshint.src.src %>'],
                    instrumentedFiles: 'jscov_temp/',
                    htmlReport: 'jscov/'
                }
            },
            files: ['<%= vars.js_tests_dir %>html/*.html']
        },
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            gruntfile: {
                src: ['Gruntfile.js']
            },
            src: {
                src: [
                    '<%= vars.src_js_dir %>*.js',
                    '<%= vars.src_js_dir %>app/*.js',
                    '!<%= vars.dest_js_templates %>'
                ]
            },
            test: {
                src: ['<% vars.js_tests_dir %>*.js']
            }
        },
        shell: {
            pytest: {
                command: 'py.test',
                options: {
                    stdout: true,
                    failOnError: true
                }
            }
        },
        handlebars: {
            compile: {
                options: {
                    namespace: 'KNET.templates',
                    wrapped: true,
                    processName: function (filename) {
                        var pieces = filename.split('/');
                        var name = pieces[pieces.length - 1].split('.');
                        return name[name.length - 2];
                    }
                },
                files: [{
                    src: '<%= vars.src_js_templates %>',
                    dest: '<%= vars.dest_js_templates %>'
                }]
            }
        },
        watch: {
            gruntfile: {
                files: ['<%= jshint.gruntfile.src %>'],
                tasks: ['jshint:gruntfile']
            },
            pytest: {
                files: ['<%= vars.src_py_dir %>**/*.py', '<%= vars.src_templates_dir %>**/*.html'],
                tasks: ['pytest']
            },
            jstest: {
                files: ['<%= vars.js_tests_dir %>**/*'],
                tasks: ['jshint:test', 'qunit']
            },
            js: {
                files: ['<%= jshint.src.src %>'],
                tasks: ['jshint:src', 'qunit']
            },
            jstemplates: {
                files: ['<%= vars.src_js_templates %>'],
                tasks: ['handlebars', 'qunit']
            }
        }
    });

    // Default task
    grunt.registerTask('default', ['jshint', 'handlebars', 'qunit', 'pytest']);

    grunt.registerTask('dev', ['default', 'watch']);

    grunt.registerTask('pytest', ['shell:pytest']);

    // Plugin tasks
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-handlebars');
    grunt.loadNpmTasks('grunt-qunit-istanbul');
    grunt.loadNpmTasks('grunt-shell');
};
