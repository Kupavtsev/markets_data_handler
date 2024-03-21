alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])
print(alien_0['points'])

alien_0 = {'color': 'green'}
alien_color = alien_0.get('color')
alien_points = alien_0.get('points')
print(alien_color)
print(alien_points)
