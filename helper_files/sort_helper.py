'''
This file holds all methods related to sorting the leaderboard
resort_member: resorts a member within the leaderboard
add_to_sorted_leaderboard: adds a member to leaderboard in sorted order
sort_array: helper method to call quicksort on array
quick_sort: uses quick sort on array
partition: partitions array for quicksort
'''
import discord
import member_helper
import time

#resorts a specific user after their score was changed
async def resort_member(leaderboard_array, member_index) -> None:
    member_score = await member_helper.get_member_score(leaderboard_array[member_index])
    self_name = await member_helper.get_member_name(leaderboard_array[member_index])
    array_len = len(leaderboard_array)
    sort_down = False

    if member_index + 1 < array_len:
        if await member_helper.get_member_score(leaderboard_array[member_index + 1]) > member_score:
            sort_down = True

    if sort_down:
        while True:
            if member_index + 1 < array_len:
                if await member_helper.get_member_score(leaderboard_array[member_index + 1]) > member_score:
                    temp = leaderboard_array[member_index]
                    leaderboard_array[member_index] = leaderboard_array[member_index + 1]
                    leaderboard_array[member_index + 1] = temp
                    member_index += 1
                else:
                    return None
            else:
                return None
    
    else:
        while True:
            if member_index - 1 > 0:
                if await member_helper.get_member_score(leaderboard_array[member_index - 1]) < member_score:
                    temp = leaderboard_array[member_index]
                    leaderboard_array[member_index] = leaderboard_array[member_index - 1]
                    leaderboard_array[member_index - 1] = temp
                    member_index -= 1
                else:
                    return None
            else:
                return None

#adds a new member to the leaderboard in sorted order
async def add_to_sorted_leaderboard(lb_list, new_member) -> None:
    member_added = False
    new_member_score = await member_helper.get_member_score(new_member)
    for index in range(len(lb_list)):
        lb_member_score = await member_helper.get_member_score(lb_list[index])
        if new_member_score >= lb_member_score:
            lb_list.insert(index,new_member)
            member_added = True
            break
    if not member_added:
        lb_list.append(new_member)

#helper method to call quicksort on array
async def sort_array(array) -> None:
    await quick_sort(array, 0, len(array)-1)

#uses quicksort on array
async def quick_sort(array, low, high) -> None:
    if low < high:
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = await partition(array, low, high)
        # Recursive call on the left of pivot
        await quick_sort(array, low, pi - 1)

        # Recursive call on the right of pivot
        await quick_sort(array, pi + 1, high)

#partitions array for quicksort 
async def partition(array, low, high) -> int:
    # choose the rightmost element as pivot
    pivot = await member_helper.get_member_score(array[high])
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if await member_helper.get_member_score(array[j]) >= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[j], array[i]) = (array[i], array[j])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1
