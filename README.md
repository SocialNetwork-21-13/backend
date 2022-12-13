# Spooky Labyrinth

# Сюжет и геймплей

Джон Крамер, более изветсный как Пила, похитил двух мужчин и устроил для них игру на выживание, проверку насколько они мужчины, суть которой выбраться из сложнейшего лабиринта не прикасаясь к розовым(не мужским) стенам.
# Кадры из игры
Ниже представлены реалистичные, то есть похожие на реальную жизнь, кадры из игры Spooky Labyrinth:

![[photo_5240283499452286664_y.jpg]]
![[photo_5240283499452286661_y (1).jpg]]
![[photo_5240283499452286662_y.jpg]]

![[photo_5240283499452286663_y.jpg]]

# Программная часть игры
В нашем проекте мы использовали библиотеку SFML, позволяющую реализовать реалистичную графикув игре:
1) Сначала мы создали карту нашего лабиринта, которое содержало множество стен, нарисованных с помощью прямоугольников![[photo_5240283499452286665_x (1).jpg]]
2) Изначально игрок создается на входе в лабиринт. Его положения в этот и последующие моменты времени определяются с помощью координат x,y.
3) В каждый момент времени помимо координат игрока, мы определяем направление, в котором он смотрим, при этом угол обзора каждого игрока равен 180 градусам.
4) Затем для каждого игрока мы посылаем множество лучей в пределах его угла обзора, которые позволяют определить расстояние до стен
5) Для каждого луча мы определяем ближайшую стену с участком которой он пересекается и сохраняем расстояние до него.
6) Для каждого полученного расстояния мы строим вертикальный прямоугольник, высота которого обратно пропорциональна расстоянию до него
7) Для отображения других пользователей попадающих в угол обзора аналогично определяем расстояние и отображаем их при помощи вертикальных прямоугольников
Также благодаря SFML в нашем проекте реализовано перемещение игроков:
Программа считывает нажатие клавиш Вверх, Вниз, Вправо, Влево, и обрабатывает их следующим образом:
	1)  При нажатии клавиш Вправо, Влево пользователь разворачивается, тем самым меняя направление обзора.
	2) При нажатии клавиш Вверх, Вниз пользователь сдвигается в соответсвии с направлением обзора.
# Мультиплеер
Для реализации мультиплеера была реализована клиент-серверная архитектура с использованием TCP сокета.
При каждом изменении расположения пользователь отправляет на сервер информацию о новом местоположении, а сервер рассылает её остальным пользователям.
Таким образом, каждый пользователь с помощью полученной информации может отображать других игроков.
