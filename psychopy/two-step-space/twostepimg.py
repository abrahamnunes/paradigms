from psychopy.visual import ImageStim

def get_images(win, units='pix', iloc='img/'):
    stim = {
        'reward' : ImageStim(win=win, image=iloc+'treasure.png', units=units),
        'noreward': ImageStim(win=win, image=iloc+'noreward.png', units=units),
        'planets' : {
            'example': ImageStim(win=win,
                                 image=iloc+'example_planets.png',
                                 units=units),
            'earth' : {
                'planet' : ImageStim(win=win,
                                     image=iloc+'earth_planet.png',
                                     units=units)
            },
            'purple' : {
                'planet' : ImageStim(win=win,
                                     image=iloc+'purple_planet.png',
                                     units=units),
                'stim1' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'purple_stim_1.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'purple_stim_1_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'purple_stim_1_sad.png',
                                      units=units)
                },
                'stim2' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'purple_stim_2.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'purple_stim_2_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'purple_stim_2_sad.png',
                                      units=units)
                }
            },
            'green' : {
                'planet' : ImageStim(win=win,
                                     image=iloc+'green_planet.png',
                                     units=units),
                'stim1' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'green_stim_1.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'green_stim_1_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'green_stim_1_sad.png',
                                      units=units)
                },
                'stim2' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'green_stim_2.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'green_stim_2_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'green_stim_2_sad.png',
                                      units=units)
                }
            },
            'red' : {
                'planet' : ImageStim(win=win,
                                     image=iloc+'red_planet.png',
                                     units=units),
                'stim1' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'red_stim_1.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'red_stim_1_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'red_stim_1_sad.png',
                                      units=units)
                },
                'stim2' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'red_stim_2.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'red_stim_2_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'red_stim_2_sad.png',
                                      units=units)
                }
            },
            'yellow' : {
                'planet' : ImageStim(win=win,
                                     image=iloc+'yellow_planet.png',
                                     units=units),
                'stim1' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'yellow_stim_1.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'yellow_stim_1_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'yellow_stim_1_sad.png',
                                      units=units)
                },
                'stim2' : {
                    'stim' : ImageStim(win=win,
                                       image=iloc+'yellow_stim_2.png',
                                       units=units),
                    'deact': ImageStim(win=win,
                                       image=iloc+'yellow_stim_2_deact.png',
                                       units=units),
                    'sad' : ImageStim(win=win,
                                      image=iloc+'yellow_stim_2_sad.png',
                                      units=units)
                }
            }
        },
        'aliens': {
            'example' : ImageStim(win=win,
                                  image=iloc+'example_aliens.png',
                                  units=units)
        },
        'rockets' : {
            'example' : ImageStim(win=win,
                                  image=iloc+'example_rockets.png',
                                  units=units),
            'rocket1' : {
                'stim' : ImageStim(win=win,
                                   image=iloc+'earth_stim_1.png',
                                   units=units),
                'deact' : ImageStim(win=win,
                                    image=iloc+'earth_stim_1_deact.png',
                                    units=units)
            },
            'rocket2' : {
                'stim' : ImageStim(win=win,
                                   image=iloc+'earth_stim_2.png',
                                   units=units),
                'deact' : ImageStim(win=win,
                                    image=iloc+'earth_stim_2_deact.png',
                                    units=units)
            }
        }
    }

    return stim
