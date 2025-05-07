import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# Fonction objective : Fonction de Rastrigin
#coords = coordinates list ([x] ou [x,y], or [x,y,z], or .....)
def rastrigin_function(coords, A=10):
    return A * len(coords) + sum([(ci ** 2 - A * np.cos(2 * np.pi * ci)) for ci in coords])


def visualize_rastrigin_3d(x_min=-5.12, x_max=5.12, y_min=-5.12, y_max=5.12, 
                          resolution=100, A=10, with_sliders=True):
    """
    Crée une visualisation 3D interactive de la fonction de Rastrigin.
    
    Args:
        x_min: Limite inférieure pour x (défaut: -5.12)
        x_max: Limite supérieure pour x (défaut: 5.12)
        y_min: Limite inférieure pour y (défaut: -5.12)
        y_max: Limite supérieure pour y (défaut: 5.12)
        resolution: Résolution du maillage (défaut: 100)
        A: Paramètre d'amplitude (défaut: 10)
        with_sliders: Ajouter des curseurs interactifs (défaut: True)
    """
    # Création de la figure et des axes 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Si on utilise des sliders, ajuster l'espace en bas
    if with_sliders:
        plt.subplots_adjust(bottom=0.25)
    
    # Création de la grille
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    X, Y = np.meshgrid(x, y)
    Z = rastrigin_function([X, Y], A)
    
    # Création de la surface
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.8)
    
    # Ajout des contours en bas de la figure
    cset = ax.contour(X, Y, Z, zdir='z', offset=Z.min(), cmap=cm.coolwarm)
    
    # Configuration des labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Rastrigin(X, Y)')
    ax.set_title('Fonction de Rastrigin en 3D')
    
    # Ajout d'une barre de couleurs
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Si demandé, ajouter les sliders interactifs
    if with_sliders:
        # Création des axes pour les sliders
        ax_zoom = plt.axes([0.25, 0.15, 0.65, 0.03])
        ax_resolution = plt.axes([0.25, 0.1, 0.65, 0.03])
        ax_amplitude = plt.axes([0.25, 0.05, 0.65, 0.03])
        
        # Création des sliders
        initial_zoom = 1
        zoom_slider = Slider(ax_zoom, 'Zoom', 1, 10, valinit=initial_zoom)
        resolution_slider = Slider(ax_resolution, 'Résolution', 10, 200, valinit=resolution, valstep=10)
        amplitude_slider = Slider(ax_amplitude, 'Amplitude (A)', 1, 20, valinit=A)
        
        # Fonction de mise à jour lors du changement des sliders
        def update(val):
            # Suppression de 'global' inutile
            # Récupération des valeurs des sliders
            zoom = zoom_slider.val
            res = int(resolution_slider.val)
            amp = amplitude_slider.val
            
            # Mise à jour des limites
            x_lim_min, x_lim_max = -5.12/zoom, 5.12/zoom
            y_lim_min, y_lim_max = -5.12/zoom, 5.12/zoom
            
            # Recréation de la grille
            x = np.linspace(x_lim_min, x_lim_max, res)
            y = np.linspace(y_lim_min, y_lim_max, res)
            X, Y = np.meshgrid(x, y)
            Z = rastrigin_function([X, Y], amp)
            
            # Effacement de l'ancienne surface
            ax.clear()
            
            # Création de la nouvelle surface
            surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.8)

            # Ajout des contours mis à jour
            cset = ax.contour(X, Y, Z, zdir='z', offset=Z.min(), cmap=cm.coolwarm)
            
            # Reconfiguration des labels
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Rastrigin(X, Y)')
            ax.set_title('Fonction de Rastrigin en 3D')
            
            # Mise à jour de la figure
            fig.canvas.draw_idle()
        
        # Connexion des sliders à la fonction de mise à jour
        zoom_slider.on_changed(update)
        resolution_slider.on_changed(update)
        amplitude_slider.on_changed(update)
    
    # Afficher la figure mais ne pas la retourner
    # plt.show()
    
    return fig


