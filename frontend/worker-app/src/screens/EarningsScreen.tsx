import React from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { earningsService } from '../services/api';
import { CompletedJob } from '../types';

export default function EarningsScreen() {
  const queryClient = useQueryClient();

  const { data: earnings, isLoading, error } = useQuery({
    queryKey: ['earnings'],
    queryFn: earningsService.getEarnings,
  });

  const onRefresh = async () => {
    await queryClient.invalidateQueries({ queryKey: ['earnings'] });
  };

  const renderEarningsCard = (title: string, amount: number, color: string) => (
    <View className={`${color} rounded-lg p-6 mb-4`}>
      <Text className="text-white text-sm font-medium mb-1">{title}</Text>
      <Text className="text-white text-3xl font-bold">
        ${amount.toFixed(2)}
      </Text>
    </View>
  );

  const renderCompletedJob = ({ item }: { item: CompletedJob }) => (
    <View className="bg-white rounded-lg shadow-sm p-4 mb-3">
      <View className="flex-row justify-between items-start mb-2">
        <Text className="text-lg font-semibold text-gray-800">
          Order #{item.id}
        </Text>
        <Text className="text-green-600 font-bold text-lg">
          +${item.earnings.toFixed(2)}
        </Text>
      </View>

      <View className="mb-2">
        <Text className="text-gray-600 text-sm mb-1">
          <Text className="font-medium">From:</Text> {item.pickup}
        </Text>
        <Text className="text-gray-600 text-sm">
          <Text className="font-medium">To:</Text> {item.dropoff}
        </Text>
      </View>

      <View className="flex-row justify-between items-center">
        <View className="bg-blue-100 px-2 py-1 rounded">
          <Text className="text-blue-800 text-xs">
            G-Value: {item.g_value.toFixed(2)}
          </Text>
        </View>
        <Text className="text-gray-500 text-sm">
          {new Date(item.completedAt).toLocaleDateString()}
        </Text>
      </View>
    </View>
  );

  if (isLoading) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50">
        <Text className="text-gray-600 text-lg">Loading earnings...</Text>
      </View>
    );
  }

  if (error || !earnings) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50 px-4">
        <Text className="text-red-600 text-lg text-center mb-4">
          Failed to load earnings
        </Text>
        <TouchableOpacity
          className="bg-blue-600 rounded-lg px-6 py-3"
          onPress={onRefresh}
        >
          <Text className="text-white font-semibold">Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-50">
      <FlatList
        data={earnings.completedJobs}
        renderItem={renderCompletedJob}
        keyExtractor={(item) => item.id}
        refreshControl={
          <RefreshControl refreshing={false} onRefresh={onRefresh} />
        }
        ListHeaderComponent={
          <View className="p-4">
            {renderEarningsCard(
              'Total Earnings',
              earnings.totalEarnings,
              'bg-gradient-to-r from-blue-600 to-blue-700'
            )}
            {renderEarningsCard(
              'This Week',
              earnings.weeklyEarnings,
              'bg-gradient-to-r from-green-600 to-green-700'
            )}

            <View className="flex-row justify-between items-center mb-4">
              <Text className="text-xl font-bold text-gray-800">
                Recent Jobs
              </Text>
              <Text className="text-gray-600 text-sm">
                {earnings.completedJobs.length} completed
              </Text>
            </View>
          </View>
        }
        contentContainerStyle={{ paddingBottom: 20 }}
        ListEmptyComponent={
          <View className="flex-1 justify-center items-center py-20">
            <Text className="text-gray-500 text-lg text-center">
              No completed jobs yet
            </Text>
            <Text className="text-gray-400 text-sm text-center mt-2">
              Complete some jobs to see your earnings here
            </Text>
          </View>
        }
      />
    </View>
  );
}
