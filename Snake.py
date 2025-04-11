import pygame
import random
import os
import sys

class JogoSnake:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 1000, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Jogo Snake Double Gangsta 2D")
        self.relogio = pygame.time.Clock()
        
        # Cores
        self.preta = (0, 0, 0)
        self.branca = (255, 255, 255)
        self.vermelha = (255, 0, 0)
        self.verde = (0, 255, 0)
        self.azul = (0, 0, 255)
        
        # Parâmetros do jogo
        self.tamanho_quadrado = 20
        self.velocidade_base = 10
        self.velocidade_jogo = self.velocidade_base
        self.pontos_para_acelerar = 5
        
        # Recursos gráficos
        self.carregar_recursos()
        
        # Highscore
        self.arquivo_highscore = "highscore.txt"
        self.highscore = self.carregar_highscore()
    
    def carregar_recursos(self):
        """Recursos Graficos"""
        try:
            # Fundo 
            self.fundo = pygame.Surface((self.largura, self.altura))
            self.fundo.fill((30, 30, 30)) 
            
            # Texturas para cobra e comida 
            self.textura_cobra = pygame.Surface((self.tamanho_quadrado, self.tamanho_quadrado))
            self.textura_cobra.fill(self.verde)
            
            self.textura_cabeca = pygame.Surface((self.tamanho_quadrado, self.tamanho_quadrado))
            self.textura_cabeca.fill(self.verde)
            
            self.textura_comida = pygame.Surface((self.tamanho_quadrado, self.tamanho_quadrado))
            self.textura_comida.fill(self.vermelha)
        except Exception as e:
            print(f"Erro ao carregar recursos: {e}")
            sys.exit(1)
    
    def carregar_highscore(self):
        """Carrega o recorde do arquivo"""
        try:
            if os.path.exists(self.arquivo_highscore):
                with open(self.arquivo_highscore, "r") as file:
                    return int(file.read())
        except:
            pass
        return 0
    
    def salvar_highscore(self, pontuacao):
        """Salva o novo recorde"""
        try:
            with open(self.arquivo_highscore, "w") as file:
                file.write(str(pontuacao))
        except:
            pass
    
    def gerar_comida(self):
        """Gera posição aleatória para a comida"""
        comida_x = round(random.randrange(0, self.largura - self.tamanho_quadrado) / float(self.tamanho_quadrado)) * float(self.tamanho_quadrado)
        comida_y = round(random.randrange(0, self.altura - self.tamanho_quadrado) / float(self.tamanho_quadrado)) * float(self.tamanho_quadrado)
        return comida_x, comida_y
    
    def desenhar_comida(self, comida_x, comida_y):
        """Desenha a comida na tela"""
        self.tela.blit(self.textura_comida, [comida_x, comida_y])
    
    def desenhar_cobra(self, pixels):
        """Desenha a cobra na tela"""
        for i, pixel in enumerate(pixels):
            if i == len(pixels) - 1:  # Cabeça
                self.tela.blit(self.textura_cabeca, [pixel[0], pixel[1]])
            else:  # Corpo
                self.tela.blit(self.textura_cobra, [pixel[0], pixel[1]])
    
    def desenhar_pontuacao(self, pontuacao):
        """Mostra a pontuação atual e o recorde"""
        fonte = pygame.font.SysFont("Helvetica", 35)
        texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, self.vermelha)
        texto_highscore = fonte.render(f"Recorde: {self.highscore}", True, self.branca)
        self.tela.blit(texto_pontos, [10, 10])
        self.tela.blit(texto_highscore, [10, 50])
    
    def selecionar_velocidade(self, tecla):
        """Define a direção da cobra"""
        if tecla == pygame.K_DOWN:
            return 0, self.tamanho_quadrado
        elif tecla == pygame.K_UP:
            return 0, -self.tamanho_quadrado
        elif tecla == pygame.K_RIGHT:
            return self.tamanho_quadrado, 0
        elif tecla == pygame.K_LEFT:
            return -self.tamanho_quadrado, 0
        return None, None
    
    def mostrar_menu(self):
        """Exibe o menu principal"""
        while True:
            self.tela.blit(self.fundo, (0, 0))
            
            fonte_titulo = pygame.font.SysFont("Helvetica", 70)
            fonte_opcoes = pygame.font.SysFont("Helvetica", 40)
            
            titulo = fonte_titulo.render("David Denis RA: F350150", True, self.verde)
            iniciar = fonte_opcoes.render("Iniciar Jogo (Enter)", True, self.branca)
            sair = fonte_opcoes.render("Sair (ESC)", True, self.branca)
            recorde = fonte_opcoes.render(f"Recorde: {self.highscore}", True, self.branca)
            
            # Posicionamento
            self.tela.blit(titulo, (self.largura//2 - titulo.get_width()//2, 100))
            self.tela.blit(iniciar, (self.largura//2 - iniciar.get_width()//2, 300))
            self.tela.blit(sair, (self.largura//2 - sair.get_width()//2, 370))
            self.tela.blit(recorde, (self.largura//2 - recorde.get_width()//2, 450))
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return True
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def mostrar_pausa(self):
        """Exibe o menu de pausa"""
        while True:
            # Fundo semi-transparente
            s = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.tela.blit(s, (0, 0))
            
            fonte = pygame.font.SysFont("Helvetica", 50)
            fonte_botao = pygame.font.SysFont("Helvetica", 35)
            
            texto_pausa = fonte.render("Jogo Pausado", True, self.branca)
            continuar = fonte_botao.render("Continuar (ESC)", True, self.verde)
            reiniciar = fonte_botao.render("Reiniciar (R)", True, self.branca)
            sair = fonte_botao.render("Sair (Q)", True, self.vermelha)
            
            # Posicionamento
            self.tela.blit(texto_pausa, (self.largura//2 - texto_pausa.get_width()//2, 200))
            self.tela.blit(continuar, (self.largura//2 - continuar.get_width()//2, 300))
            self.tela.blit(reiniciar, (self.largura//2 - reiniciar.get_width()//2, 370))
            self.tela.blit(sair, (self.largura//2 - sair.get_width()//2, 440))
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "continuar"
                    elif evento.key == pygame.K_r:
                        return "reiniciar"
                    elif evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    
    def tela_game_over(self, pontuacao):
        """Exibe a tela de game over"""
        while True:
            self.tela.blit(self.fundo, (0, 0))
            
            fonte = pygame.font.SysFont("Helvetica", 50)
            fonte_botao = pygame.font.SysFont("Helvetica", 35)
            
            texto_game_over = fonte.render("Game Over", True, self.vermelha)
            texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, self.branca)
            texto_recorde = fonte.render(f"Recorde: {self.highscore}", True, self.verde)
            
            reiniciar = fonte_botao.render("Reiniciar (R)", True, self.branca)
            sair = fonte_botao.render("Sair (Q)", True, self.vermelha)
            
            # Posicionamento
            self.tela.blit(texto_game_over, (self.largura//2 - texto_game_over.get_width()//2, 150))
            self.tela.blit(texto_pontuacao, (self.largura//2 - texto_pontuacao.get_width()//2, 230))
            self.tela.blit(texto_recorde, (self.largura//2 - texto_recorde.get_width()//2, 300))
            self.tela.blit(reiniciar, (self.largura//2 - reiniciar.get_width()//2, 400))
            self.tela.blit(sair, (self.largura//2 - sair.get_width()//2, 470))
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        return "reiniciar"
                    elif evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    
    def rodar_jogo(self):
        """Loop principal do jogo"""
        while True:
            if not self.mostrar_menu():
                break
            
            # Reinicia os valores do jogo
            x = self.largura / 2
            y = self.altura / 2
            velocidade_x = 0
            velocidade_y = 0
            tamanho_cobra = 1
            pixels = []
            comida_x, comida_y = self.gerar_comida()
            self.velocidade_jogo = self.velocidade_base
            fim_jogo = False
            
            while not fim_jogo:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            acao = self.mostrar_pausa()
                            if acao == "reiniciar":
                                fim_jogo = True
                                break
                            elif acao == "continuar":
                                continue
                        else:
                            vx, vy = self.selecionar_velocidade(evento.key)
                            if vx is not None and vy is not None:
                                # Evita movimento inverso imediato
                                if not (velocidade_x and vx == -velocidade_x) and not (velocidade_y and vy == -velocidade_y):
                                    velocidade_x, velocidade_y = vx, vy
                
                if fim_jogo:
                    break
                
                # Atualiza posição
                x += velocidade_x
                y += velocidade_y
                
                # Verifica colisões com as bordas
                if x < 0 or x >= self.largura or y < 0 or y >= self.altura:
                    fim_jogo = True
                
                # Atualiza corpo da cobra
                pixels.append([x, y])
                if len(pixels) > tamanho_cobra:
                    del pixels[0]
                
                # Verifica colisão com o próprio corpo
                for pixel in pixels[:-1]:
                    if pixel == [x, y]:
                        fim_jogo = True
                
                # Desenha tudo
                self.tela.blit(self.fundo, (0, 0))
                self.desenhar_comida(comida_x, comida_y)
                self.desenhar_cobra(pixels)
                self.desenhar_pontuacao(tamanho_cobra - 1)
                pygame.display.update()
                
                # Verifica se comeu a comida
                if x == comida_x and y == comida_y:
                    tamanho_cobra += 1
                    comida_x, comida_y = self.gerar_comida()
                    
                    # Aumenta velocidade a cada 5 pontos
                    if (tamanho_cobra - 1) % self.pontos_para_acelerar == 0:
                        self.velocidade_jogo += 1
                
                self.relogio.tick(self.velocidade_jogo)
            
            # Atualiza recorde se necessário
            if tamanho_cobra - 1 > self.highscore:
                self.highscore = tamanho_cobra - 1
                self.salvar_highscore(self.highscore)
            
            # Mostra tela de game over
            acao = self.tela_game_over(tamanho_cobra - 1)
            if acao == "reiniciar":
                continue
            else:
                break

# Inicia o jogo
if __name__ == "__main__":
    jogo = JogoSnake()
    jogo.rodar_jogo()
    pygame.quit()
