/*
 * Bootstrap Image Gallery JS Demo
 * https://github.com/blueimp/Bootstrap-Image-Gallery
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*global blueimp, $ */

$(function () {
  'use strict'


  //$('#borderless-checkbox').on('change', function () {
  //  var borderless = $(this).is(':checked')
  //  $('#blueimp-gallery').data('useBootstrapModal', !borderless)
  //  $('#blueimp-gallery').toggleClass('blueimp-gallery-controls', borderless)
  //})

  //$('#fullscreen-checkbox').on('change', function () {
  //  $('#blueimp-gallery').data('fullScreen', $(this).is(':checked'))
  //})

  $('#image-gallery-button').on('click', function (event) {
    event.preventDefault()
    blueimp.Gallery($('#links a'), $('#blueimp-gallery').data())
  })

})
