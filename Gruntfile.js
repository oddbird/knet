/*global module:false*/
module.exports = function (grunt) {

    'use strict';

    // Project configuration.
    grunt.initConfig({
        vars: {
            src_py_dir: 'knet/',
            src_templates_dir: 'templates/',
            src_js_dir: 'static/js/',
            js_tests_dir: 'jstests/'
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
                src: ['<%= vars.src_js_dir %>*.js']
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
            }
        }
    });

    // Default task
    grunt.registerTask('default', ['jshint', 'qunit', 'pytest']);

    grunt.registerTask('dev', ['default', 'watch']);

    grunt.registerTask('pytest', ['shell:pytest']);

    // Plugin tasks
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-qunit-istanbul');
    grunt.loadNpmTasks('grunt-shell');
};
