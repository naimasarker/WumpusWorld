import sys
import subprocess
import os
from Map import *
from Agent import *
import Algorithms
from Specification import *  

class Graphic:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.caption = pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.map = None
        self.agent = None
        self.gold = None
        self.wumpus = None
        self.pit = None
        self.arrow = None
        self.font = pygame.font.Font(FONT_MRSMONSTER, 30)
        self.noti = pygame.font.Font(FONT_MRSMONSTER, 15)
        self.victory = pygame.font.Font(FONT_MRSMONSTER, 50)
        self.all_sprites = pygame.sprite.Group()

        self.state = MAP
        self.map_i = 1
        self.mouse = None
        # Use absolute path for background image
        bg_path = os.path.join(BASE_DIR, 'Assets', 'Images', 'win.jpg')
        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.direct = 3

    def home_draw(self):
        screen_width, screen_height = self.screen.get_size()
        for y in range(screen_height):
            ratio = y / screen_height
            r = int(139 + ratio * 30)
            g = int(69 + ratio * 50)
            b = int(19 + ratio * 20)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (screen_width, y))

    def draw_button(self, surf, rect, is_hover, text):
        base_color = (160, 82, 45)
        hover_color = (205, 133, 63)
        text_color = (255, 255, 240)
        button_color = hover_color if is_hover else base_color
        pygame.draw.rect(surf, button_color, rect, border_radius=10)
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surf.blit(text_surf, text_rect)

    def reload_maps(self):
        """Reload the map specifications"""
        from importlib import reload
        import Specification
        reload(Specification)
        global MAP_LIST, OUTPUT_LIST
        MAP_LIST = Specification.MAP_LIST
        OUTPUT_LIST = Specification.OUTPUT_LIST


    def home_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(mouse_pos):
                        if i < 5:  # MAP 1 to MAP 5
                            self.state = RUNNING
                            self.map_i = i + 1
                            return
                        elif i == 5:  # CUSTOM MAP
                            custom_map_path = os.path.join("Assets", "Input", "custom_map.txt")
                            if os.path.exists(custom_map_path):
                                self.state = RUNNING
                                self.map_i = "custom"
                                return
                            else:
                                print("Custom map not found! Please create one first.")
                        elif i == 6:  # CREATE MAP
                            current_dir = os.path.dirname(os.path.abspath(__file__))
                            map_editor_path = os.path.join(current_dir, 'map_editor.py')
                            if os.path.exists(map_editor_path):
                                subprocess.call([sys.executable, map_editor_path])
                            else:
                                parent_dir = os.path.dirname(current_dir)
                                map_editor_path = os.path.join(parent_dir, 'map_editor.py')
                                if os.path.exists(map_editor_path):
                                    subprocess.call([sys.executable, map_editor_path])
                                else:
                                    print(f"Error: map_editor.py not found in {current_dir} or {parent_dir}")
                                    return
                            self.reload_maps()  # Reload maps after editor closes
                        elif i == 7:  # EXIT
                            pygame.quit()
                            sys.exit()

        self.mouse = pygame.mouse.get_pos()
        pygame.display.update()

    def load_custom_map(self):
        """Load custom map from file"""
        custom_map_path = os.path.join("Assets", "Input", "custom_map.txt")
        custom_output_path = os.path.join("Assets", "Output", "custom_result.txt")
        
        if not os.path.exists(custom_map_path):
            print("Custom map file not found!")
            return None, None
            
        try:
            with open(custom_map_path, 'r') as f:
                lines = f.readlines()
                
            # Parse the file
            size = int(lines[0].strip())
            map_data = []
            
            for i in range(1, size + 1):
                row = lines[i].strip().split('.')
                map_data.append(row)
            
            # Check if output file exists, if not create empty one
            if not os.path.exists(custom_output_path):
                with open(custom_output_path, 'w') as f:
                    f.write("")
            
            return map_data, custom_output_path
            
        except Exception as e:
            print(f"Error loading custom map: {e}")
            return None, None

    def run(self):
        while True:
            if self.state == MAP:
                self.home_draw()
                self.home_event()

            elif self.state == RUNNING:
                self.state = TRYBEST

                # Handle custom map
                if self.map_i == "custom":
                    custom_map_path = os.path.join("Assets", "Input", "custom_map.txt")
                    custom_output = os.path.join("Assets", "Output", "custom_result.txt")
                    if not os.path.exists(custom_map_path):
                        print("Custom map file not found!")
                        self.state = MAP
                        continue
                    
                    # Pass the file path instead of parsed map data
                    action_list, cave_cell, cell_matrix = Algorithms.AgentBrain(custom_map_path, custom_output).solve_wumpus_world()
                else:
                    # Use regular map
                    action_list, cave_cell, cell_matrix = Algorithms.AgentBrain(MAP_LIST[self.map_i - 1], OUTPUT_LIST[self.map_i - 1]).solve_wumpus_world()
                
                map_pos = cave_cell.map_pos
            # ... rest of the code remains unchanged

                self.map = Map((len(cell_matrix) - map_pos[1] + 1, map_pos[0]))
                self.arrow = Arrow()
                self.gold = Gold()
                self.agent = Agent(len(cell_matrix) - map_pos[1] + 1, map_pos[0])
                self.agent.load_image()
                self.all_sprites = pygame.sprite.Group()
                self.all_sprites.add(self.agent)

                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_pit():
                            x.append(ir)
                            y.append(ic)
                self.pit = Pit(x, y)
                self.pit.pit_notification()

                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_wumpus():
                            x.append(ir)
                            y.append(ic)
                self.wumpus = Wumpus(x, y)
                self.wumpus.wumpus_notification()

                self.running_draw()

                for action in action_list:
                    pygame.time.delay(SPEED)
                    self.display_action(action)

                    if action == Algorithms.Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD:
                        self.state = WIN

                    if action == Algorithms.Action.FALL_INTO_PIT or action == Algorithms.Action.BE_EATEN_BY_WUMPUS:
                        self.state = GAMEOVER
                        break

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        # elif event.type == pygame.USEREVENT:
                        #     self.action_text = ""

            elif self.state == WIN or self.state == TRYBEST:
                self.win_draw()
                self.win_event()

            self.clock.tick(60)

   
    def win_draw(self):
        # Fill with new background color
        self.screen.fill((135, 206, 235))  # Changed to new blue color
        # self.screen.blit(self.bg, (0, 0))  # Comment out or remove background image if not needed
        
        if self.state == WIN:
            text = self.victory.render('VICTORY!!!', True, BLACK)
        elif self.state == TRYBEST:
            text = self.victory.render('TRY BEST!!!', True, BLACK)

        textRect = text.get_rect()
        textRect.center = (500, 50)
        self.screen.blit(text, textRect)
        score = self.agent.get_score()
        text = self.victory.render('Your score: ' + str(score), True, BLACK)
        textRect.center = (450, 100)
        self.screen.blit(text, textRect)

    def win_event(self):
        start_time = pygame.time.get_ticks()  # Record the start time in milliseconds
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Transition to MAP state if the user clicks
                    self.state = MAP
                    return

            # Check if 1 minute (60,000 milliseconds) has elapsed
            current_time = pygame.time.get_ticks()
            if current_time - start_time >= 60000:  # 60,000 ms = 1 minute
                self.state = MAP
                return

            pygame.display.update()
            self.clock.tick(60)  # Maintain 60 FPS to keep the window responsive

    def display_action(self, action: Algorithms.Action):

        if action == Algorithms.Action.TURN_LEFT:
            self.direct = self.agent.turn_left()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.TURN_RIGHT:
            self.direct = self.agent.turn_right()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.TURN_UP:
            self.direct = self.agent.turn_up()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.TURN_DOWN:
            self.direct = self.agent.turn_down()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.MOVE_FORWARD:
            self.agent.move_forward(self.direct)
            i, j = self.agent.get_pos()
            self.map.discover_cell_i_j(i, j)
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.GRAB_GOLD:
            self.agent.grab_gold()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            self.gold.grab_gold(self.screen, self.font)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.PERCEIVE_BREEZE:
            pass
        elif action == Algorithms.Action.PERCEIVE_STENCH:
            pass
        elif action == Algorithms.Action.SHOOT:
            self.agent.shoot()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            i, j = self.agent.get_pos()
            self.arrow.shoot(self.direct, self.screen, i, j)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.KILL_WUMPUS:
            i, j = self.agent.get_pos()
            if self.direct == 0:
                i -= 1
            elif self.direct == 1:
                i += 1
            elif self.direct == 2:
                j -= 1
            elif self.direct == 3:
                j += 1
            self.wumpus.wumpus_killed(i, j)
            self.wumpus.wumpus_notification()
            i, j = self.agent.get_pos()
            if not self.wumpus.stench_i_j(i, j):
                self.wumpus.wumpus_kill(self.screen, self.font)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
            pass
        elif action == Algorithms.Action.KILL_NO_WUMPUS:
            pass
        elif action == Algorithms.Action.BE_EATEN_BY_WUMPUS:
            self.agent.wumpus_or_pit_collision()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.state = GAMEOVER
        elif action == Algorithms.Action.FALL_INTO_PIT:
            self.agent.wumpus_or_pit_collision()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.state = GAMEOVER
        elif action == Algorithms.Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD:
            self.state = WIN
            pass
        elif action == Algorithms.Action.CLIMB_OUT_OF_THE_CAVE:
            self.agent.climb()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            self.map.agent_climb(self.screen, self.font)
            pygame.display.update()
            pygame.time.delay(2000)
        elif action == Algorithms.Action.DECTECT_PIT:
            i, j = self.agent.get_pos()
            if self.direct == 0:
                i -= 1
            elif self.direct == 1:
                i += 1
            elif self.direct == 2:
                j -= 1
            elif self.direct == 3:
                j += 1
            self.map.pit_detect(i, j)
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            pygame.time.delay(1000)
        elif action == Algorithms.Action.DETECT_WUMPUS:
            pass
        elif action == Algorithms.Action.DETECT_NO_PIT:
            pass
        elif action == Algorithms.Action.DETECT_NO_WUMPUS:
            pass
        elif action == Algorithms.Action.INFER_PIT:
            pass
        elif action == Algorithms.Action.INFER_NOT_PIT:
            pass
        elif action == Algorithms.Action.INFER_WUMPUS:
            pass
        elif action == Algorithms.Action.INFER_NOT_WUMPUS:
            pass
        elif action == Algorithms.Action.DETECT_SAFE:
            pass
        elif action == Algorithms.Action.INFER_SAFE:
            pass
        else:
            raise TypeError("Error: " + self.display_action.__name__)

