import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Alert,
  ScrollView,
} from 'react-native';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { orderService } from '../services/api';
import { Order } from '../types';

export default function CurrentJobScreen() {
  const queryClient = useQueryClient();

  const { data: orders = [] } = useQuery({
    queryKey: ['orders'],
    queryFn: orderService.getOrders,
  });

  const completeOrderMutation = useMutation({
    mutationFn: orderService.completeOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['earnings'] });
      Alert.alert('Success', 'Job completed successfully!');
    },
    onError: (error) => {
      Alert.alert('Error', 'Failed to complete job. Please try again.');
    },
  });

  // Find the current active job (accepted but not completed)
  const currentJob = orders.find(order => order.status === 'accepted');

  const handleCompleteJob = () => {
    if (!currentJob) return;

    Alert.alert(
      'Complete Job',
      'Are you sure you want to mark this job as complete?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Complete', 
          onPress: () => completeOrderMutation.mutate(currentJob.id) 
        },
      ]
    );
  };

  if (!currentJob) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50 px-4">
        <View className="bg-white rounded-lg shadow-lg p-8 items-center">
          <Text className="text-6xl mb-4">📦</Text>
          <Text className="text-xl font-semibold text-gray-800 mb-2">
            No Active Job
          </Text>
          <Text className="text-gray-600 text-center mb-6">
            You don't have any active jobs at the moment.{'\n'}
            Check the Orders tab to find available jobs.
          </Text>
          <TouchableOpacity
            className="bg-blue-600 rounded-lg px-6 py-3"
            onPress={() => {
              // Navigate to Orders tab
              // This would typically be handled by navigation
            }}
          >
            <Text className="text-white font-semibold">View Available Jobs</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-gray-50">
      <View className="p-4">
        <View className="bg-white rounded-lg shadow-lg p-6 mb-4">
          <View className="flex-row justify-between items-start mb-4">
            <Text className="text-2xl font-bold text-gray-800">
              Order #{currentJob.id}
            </Text>
            <View className="bg-green-100 px-3 py-1 rounded-full">
              <Text className="text-green-800 text-sm font-medium">
                In Progress
              </Text>
            </View>
          </View>

          <View className="mb-6">
            <View className="mb-4">
              <Text className="text-gray-600 text-sm mb-1 font-medium">
                PICKUP LOCATION
              </Text>
              <Text className="text-gray-800 text-lg">
                {currentJob.pickup}
              </Text>
            </View>

            <View className="mb-4">
              <Text className="text-gray-600 text-sm mb-1 font-medium">
                DROPOFF LOCATION
              </Text>
              <Text className="text-gray-800 text-lg">
                {currentJob.dropoff}
              </Text>
            </View>
          </View>

          <View className="bg-gray-50 rounded-lg p-4 mb-6">
            <Text className="text-gray-600 text-sm mb-2 font-medium">
              JOB DETAILS
            </Text>
            <View className="flex-row justify-between mb-2">
              <Text className="text-gray-600">Estimated Time:</Text>
              <Text className="text-gray-800 font-medium">
                {currentJob.eta} minutes
              </Text>
            </View>
            <View className="flex-row justify-between mb-2">
              <Text className="text-gray-600">G-Value:</Text>
              <Text className="text-gray-800 font-medium">
                {currentJob.g_mean.toFixed(2)}
              </Text>
            </View>
            <View className="flex-row justify-between">
              <Text className="text-gray-600">Variance:</Text>
              <Text className="text-gray-800 font-medium">
                {currentJob.g_var.toFixed(2)}
              </Text>
            </View>
          </View>

          <TouchableOpacity
            className="bg-green-600 rounded-lg py-4"
            onPress={handleCompleteJob}
            disabled={completeOrderMutation.isPending}
          >
            <Text className="text-white text-center text-lg font-semibold">
              {completeOrderMutation.isPending ? 'Completing...' : 'Mark as Complete'}
            </Text>
          </TouchableOpacity>
        </View>

        <View className="bg-blue-50 rounded-lg p-4">
          <Text className="text-blue-800 text-sm text-center">
            💡 Tip: Make sure to confirm delivery with the customer before marking as complete
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}
