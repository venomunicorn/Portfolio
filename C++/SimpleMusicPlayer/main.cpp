#include <iostream>
#include <windows.h> // Beep

// C++ Simple Music Player (Windows Beep)
// Plays a melody using system speakers

// Frequencies (Hz)
#define NOTE_C4  261
#define NOTE_D4  294
#define NOTE_E4  329
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  493
#define NOTE_C5  523

int main() {
    std::cout << "--- Simple Music Player ---" << std::endl;
    std::cout << "Playing 'Twinkle Twinkle Little Star'..." << std::endl;
    
    int melody[] = {
        NOTE_C4, NOTE_C4, NOTE_G4, NOTE_G4, NOTE_A4, NOTE_A4, NOTE_G4,
        NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_D4, NOTE_D4, NOTE_C4
    };
    
    int durations[] = {
        500, 500, 500, 500, 500, 500, 1000,
        500, 500, 500, 500, 500, 500, 1000
    };
    
    for (int i = 0; i < 14; i++) {
        std::cout << "Note: " << melody[i] << "Hz" << std::endl;
        Beep(melody[i], durations[i]);
    }
    
    std::cout << "Playback Finished." << std::endl;
    return 0;
}
